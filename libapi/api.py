#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urlparse
import requests
import logging
import sys
from libapi.login_exception import LoginException
import urllib3

reload(sys)
sys.setdefaultencoding('utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger()

class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value


class UJNLibApi(object):
    def __init__(self, *account):
        l = len(account)
        self.base_url = 'https://seat.ujn.edu.cn:8443'
        self.api = {
            'getToken': 'rest/auth?username={}&password={}',
            'checkToken': 'rest/v2/user/reservations?token={}',
            'getDatetime': 'rest/v2/free/filters',
            'building': 'rest/v2/room/stats2/2?token={}',
            'getSeatStartTime': 'rest/v2/startTimesForSeat/{}/{}?token={}',
            'quickBook': 'rest/v2/quickBook',
            'freeBook': 'rest/v2/freeBook',
            'layoutByDate': 'rest/v2/room/layoutByDate/{}/{}/?token={}',
            'checkIn': 'rest/v2/checkIn?token={}',
            'exit': 'rest/v2/stop?token={}',
            'getMaxTime': 'rest/v2/allowedHours?token={}',
            'getHistory': 'rest/v2/history/{}/{}?token={}',
            'cancelRes': 'rest/v2/cancel/{}?token={}'
        }
        if l == 0:
            self.ac = '220141222001'
            self.pw = '100325'
        elif l == 1:
            self.ac = self.pw = account[0]
        else:
            self.ac = account[0]
            self.pw = account[1]
        self.token = self.getToken()
        self.dates = self.getDatetime()
        self.date = self.dates[0]

    def parse_json(self, json_str):
        """parse str into JsonDict"""

        def _obj_hook(pairs):
            """convert json object to python object"""
            o = JsonDict()
            for k, v in pairs.items():
                o[str(k)] = v
            return o

        return json.loads(json_str, object_hook=_obj_hook)

    def requests_call(self, method, url, headers={}, params=None, data=None, stream=False, verify=False):
        if (method == 'GET'):
            return requests.get(url, params=params, headers=headers, stream=stream, verify=False)
        elif (method == 'POST'):
            return requests.post(url, params=params, data=data, headers=headers, stream=stream, verify=False)
        elif (method == 'DELETE'):
            return requests.delete(url, params=params, data=data, headers=headers, stream=stream, verify=False)

    def getToken(self):
        # 获取token
        logger.info(self.ac + ": 登录")
        param = self.api['getToken'].format(self.ac, self.pw)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        page_json = json.loads(r.text)
        if page_json['status'] == 'success':
            return page_json['data']['token']
        else:
            raise LoginException(self.ac, self.pw, page_json['message'])

    def checkToken(self):
        # 检测token是否过期
        param = self.api['checkToken'].format(self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        page = r.text
        if page.find('success') == -1:
            return False
        else:
            return True

    def setDate(self, choose):
        # 设置预约日期
        if choose == '2' or choose.lower() == 'y':
            self.date = self.dates[1]
        else:
            self.date = self.dates[0]

    def getDatetime(self):
        # 获取日期
        param = self.api['getDatetime']
        url = urlparse.urljoin(self.base_url, param)
        data = {'token': self.token}
        r = self.requests_call('POST', url, data=data)
        page_json = json.loads(r.text)
        date = page_json['data']['dates']
        return date

    def building(self):
        # 获取楼层信息
        param = self.api['building'].format(self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def getSeatStartTime(self, seat_id):
        # return a list contain tuple for web
        param = self.api['getSeatStartTime'].format(seat_id, self.date, self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def quickBook(self, hour, building='2'):
        # 快速预约
        param = self.api['quickBook']
        url = urlparse.urljoin(self.base_url, param)
        post_data = {
            "token": self.token,
            "building": building,
            "hour": hour
        }
        r = self.requests_call('POST', url, data=post_data)
        return self.parse_json(r.text)

    def freeBook(self, start_time, end_time, seat_id):
        # 预约座位
        param = self.api['freeBook']
        url = urlparse.urljoin(self.base_url, param)
        start = int(start_time) * 60
        end = int(end_time) * 60
        post_data = {
            'token': self.token,
            'startTime': str(start),
            'endTime': str(end),
            'seat': seat_id,
            'date': self.date
        }
        r = self.requests_call('POST', url, data=post_data)
        return self.parse_json(r.text)

    def layoutByDate(self, room_id):
        param = self.api['layoutByDate'].format(room_id, self.date, self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def checkIn(self):
        # 签到
        param = self.api['checkIn'].format(self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def exit(self):
        # 退出登录
        param = self.api['exit'].format(self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def getMaxTime(self):
        # 获取最大可预约时间
        param = self.api['getMaxTime'].format(self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def getHistory(self, page=1, count=10):
        # 获取预约历史
        # 1是页数从1开始 10为每页显示个数
        param = self.api['getHistory'].format(page, count, self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def cancelRes(self, resid):
        param = self.api['cancelRes'].format(resid, self.token)
        url = urlparse.urljoin(self.base_url, param)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)


if __name__ == '__main__':
    pass
