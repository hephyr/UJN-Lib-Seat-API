#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


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
        if l == 0:
            self.ac = self.pw = '220141222001'
        elif l == 1:
            self.ac = self.pw = account[0]
        else:
            self.ac = account[0]
            self.pw = account[1]
        self.token = self.getToken()
        self.dates = self.getDatetime()
        self.date = self.dates[0]
        if self.token is False:
            return False

    def parse_json(self, json_str):
        """parse str into JsonDict"""

        def _obj_hook(pairs):
            """convert json object to python object"""
            o = JsonDict()
            for k, v in pairs.items():
                o[str(k)] = v
            return o

        return json.loads(json_str, object_hook=_obj_hook)

    def requests_call(self, method, url, headers={}, params=None, data=None, stream=False):
        headers['Client-Ip'] = '172.16.219.219'
        headers['X-Forwarded-For'] = '172.16.219.219'
        if (method == 'GET'):
            return requests.get(url, params=params, headers=headers, stream=stream)
        elif (method == 'POST'):
            return requests.post(url, params=params, data=data, headers=headers, stream=stream)
        elif (method == 'DELETE'):
            return requests.delete(url, params=params, data=data, headers=headers, stream=stream)

    def getToken(self):
        # 获取token
        url = 'http://seat.ujn.edu.cn/rest/auth?username=%s&password=%s' % (self.ac, self.pw)
        r = self.requests_call('GET', url)
        page_json = json.loads(r.text)
        if page_json['status'] == 'success':
            return page_json['data']['token']
        else:
            raise TypeError('Wrong account or password')

    def checkToken(self):
        # 检测token是否过期
        url = 'http://seat.ujn.edu.cn/rest/v2/user/reservations?token=%s' % self.token
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
        url = 'http://seat.ujn.edu.cn/rest/v2/free/filters'
        data = {'token': self.token}
        r = self.requests_call('POST', url, data=data)
        page_json = json.loads(r.text)
        date = page_json['data']['dates']
        return date

    def building(self):
        # 获取楼层信息
        url = 'http://seat.ujn.edu.cn/rest/v2/room/stats2/2?token=%s' % self.token
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def getSeatStartTime(self, seat_id):
        # return a list contain tuple for web
        url = 'http://seat.ujn.edu.cn/rest/v2/startTimesForSeat/%s/%s?token=%s' % (seat_id, self.date, self.token)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def quickBook(self, hour, building='2'):
        # 快速预约
        post_data = {
            "token": self.token,
            "building": building,
            "hour": hour
        }
        url = 'http://seat.ujn.edu.cn/rest/v2/quickBook'
        r = self.requests_call('POST', url, data=post_data)
        return self.parse_json(r.text)

    def freeBook(self, start_time, end_time, seat_id):
        # 预约座位
        start = int(start_time) * 60
        end = int(end_time) * 60
        url = 'http://seat.ujn.edu.cn/rest/v2/freeBook'
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
        url = 'http://seat.ujn.edu.cn/rest/v2/room/layoutByDate/%s/%s/?token=%s' % (room_id, self.date, self.token)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def checkIn(self):
        # 签到
        url = 'http://seat.ujn.edu.cn/rest/v2/checkIn?token=%s' % self.token
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def exit(self):
        # 退出登录
        url = 'http://seat.ujn.edu.cn/rest/v2/stop?token=%s' % self.token
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def getMaxTime(self):
        # 获取最大可预约时间
        url = 'http://seat.ujn.edu.cn/rest/v2/allowedHours?token=%s' % self.token
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def getHistory(self, page=1, count=10):
        # 获取预约历史
        # 1是页数从1开始 10为每页显示个数
        url = 'http://seat.ujn.edu.cn/rest/v2/history/%d/%d?token=%s' % (page, count, self.token)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)

    def cancelRes(self, resid):
        url = 'http://seat.ujn.edu.cn/rest/v2/cancel/%s?token=%s' % (resid, self.token)
        r = self.requests_call('GET', url)
        return self.parse_json(r.text)


def main():
    pass


if __name__ == '__main__':
    main()
