#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from .utils import LoginException, parse_json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class leoapi(object):
    def __init__(self, *account):
        l = len(account)
        self.base_url = 'https://seat.ujn.edu.cn:8443'
        self.api = {
            'token': '/rest/auth?username={username}&password={password}',
            'user': '/rest/v2/user',
            'filters': '/rest/v2/free/filters',
            'checkIn': '/rest/v2/checkIn',
            'reservations': '/rest/v2/user/reservations',
            'roomStats': '/rest/v2/room/stats2/{building}',
            'layoutByDate': '/rest/v2/room/layoutByDate/{room}/{date}/',
            'seatStartTime': '/rest/v2/startTimesForSeat/{id}/{date}',
            'seatEndTime': '/rest/v2/endTimesForSeat/{id}/{date}/{start}',
            'history': '/rest/v2/history/{page}/{count}',
            'cancelRes': '/rest/v2/cancel/{id}',
            'freeBook': '/rest/v2/freeBook'
        }
        for i in self.api:
            self.api[i] = self.base_url + self.api[i]
        if l == 0:
            pass
        elif l == 1:
            self.ac = self.pw = account[0]
        else:
            self.ac = account[0]
            self.pw = account[1]
        self.token = ''
        self.login()


    def requests_call(self, method, url, headers={}, params=None, data=None, stream=False, verify=False):
        if (method == 'GET'):
            return requests.get(url, params=params, headers=headers, stream=stream, verify=False)
        elif (method == 'POST'):
            return requests.post(url, params=params, data=data, headers=headers, stream=stream, verify=False)
        elif (method == 'DELETE'):
            return requests.delete(url, params=params, data=data, headers=headers, stream=stream, verify=False)
    
    def requests(self, method, url, data=None, params=None):
        headers = {
            'Host': 'seat.ujn.edu.cn:8443',
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "token": self.token,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
            'Accept-Encoding': 'gzip',
            'X-Forwarded-For': '10.167.159.118'
        }
        return self.requests_call(method, url, headers=headers, data=data, params=params)

    def login(self):
        d = self.getToken()
        if d.status == 'success':
            self.token = d.data.token
        elif d.status == 'fail':
            raise LoginException(self.ac, self.pw, d.message)

    def getToken(self):
        # 获取token
        r = self.requests_call("GET", self.api['token'].format(username=self.ac, password=self.pw))
        return parse_json(r.text)

    def reservations(self):
        # 查看预约
        r = self.requests('GET', self.api['reservations'])
        return parse_json(r.text)


    def user(self):
        # 用户信息
        r = self.requests('GET', self.api['user'])
        return parse_json(r.text)

    def filters(self):
        # 图书馆信息
        r = self.requests('GET', self.api['filters'])
        return parse_json(r.text)

    def roomStats(self, building_id):
        # 获取楼层信息
        r = self.requests("GET", self.api['roomStats'].format(building=building_id))
        return parse_json(r.text)

    def seatStartTime(self, seat_id, date):
        # 可开始时间
        url = self.api['seatStartTime'].format(id=seat_id, date=date)
        r = self.requests('GET', url)
        return parse_json(r.text)

    def seatEndTime(self, seat_id, date, start_time):
        # 结束时间
        url = self.api['seatEndTime'].format(id=seat_id, date=date, start=start_time)
        r = self.requests('GET', url)
        return parse_json(r.text)

    def freeBook(self, start_time, end_time, seat_id, date):
        # 预约座位

        if float(start_time) <= 24:
            start = float(start_time) * 60
            end = float(end_time) * 60
        post_data = {
            'startTime': str(int(start)),
            'endTime': str(int(end)),
            'seat': seat_id,
            'date': date
        }
        r = self.requests('POST', self.api["freeBook"], data=post_data)
        return parse_json(r.text)

    def layoutByDate(self, room_id, date):
        url = self.api['layoutByDate'].format(room=room_id, date=date)
        r = self.requests('GET', url)
        return parse_json(r.text)

    def checkIn(self):
        # 签到
        r = self.requests('GET', self.api['checkIn'])
        return parse_json(r.text)

    def history(self, page=1, count=10):
        # 获取预约历史
        # 1是页数从1开始 10为每页显示个数
        url = self.api['history'].format(page=page, count=count)
        r = self.requests('GET', url)
        return parse_json(r.text)

    def cancelRes(self, res_id):
        r = self.requests('GET', self.api['cancelRes'].format(id=res_id))
        return parse_json(r.text)


if __name__ == '__main__':
    pass
