#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
import random
import requests


class PersonLib(object):
    def __init__(self, *account):
        base_url = 'http://seat.ujn.edu.cn/'
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

    def getToken(self):
        url = 'http://seat.ujn.edu.cn/rest/auth?username=%s&password=%s' % (self.ac, self.pw)
        r = requests.get(url)
        page_json = json.loads(r.text)
        if page_json['status'] == 'success':
            return page_json['data']['token']
        else:
            raise TypeError('Wrong account or password')

    def checkToken(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/user/reservations?token=%s' % self.token
        r = requests.get(url)
        page = r.text
        if page.find('success') == -1:
            return False
        else:
            return True

    def getDatetime(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/free/filters'
        data = {'token': self.token}
        r = requests.post(url, data)
        page_json = json.loads(r.text)
        date = page_json['data']['dates']
        return date

    def getBuildingsInfo(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/room/stats2/2?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        if page_json['status'] == 'success':
            data = ''
            for value in page_json['data']:
                data += 'id:' + str(value['roomId']) + value['room']
                data += u' 楼层:' + str(value['floor'])
                data += u' 剩余:' + str(value['free']) + '\n'
            return data
        else:
            return page_json['message']

    def getSeatTime(self, seat_id):
        url = 'http://seat.ujn.edu.cn/rest/v2/startTimesForSeat/%s/%s?token=%s' % (seat_id, self.date, self.token)
        r = requests.get(url)
        page_json = json.loads(r.text)
        text = '可开始时间\n'
        for i in page_json['data']['startTimes']:
            text += str(i['value']) + '\n'
        return text

    def quickBook(self, hour):
        post_data = {
            "token": self.token,
            "building": "2",
            "hour": hour
        }
        url = 'http://seat.ujn.edu.cn/rest/v2/quickBook'
        r = requests.post(url, post_data)
        page_json = json.loads(r.text)
        data = ''
        if page_json['status'] != 'success':
            data = '预约失败' + page_json['message']
            return data
        else:
            data += '日期: ' + page_json['data']['reservation']['onDate'] + '/n'
            data += '开始时间: ' + page_json['data']['reservation']['begin'] + '/n'
            data += '结束时间: ', page_json['data']['reservation']['end'] + '/n'
            data += '地点: ', page_json['data']['reservation']['location'] + '/n'
            return data + page_json['message']

    def freeBook(self, start_time, end_time, seat_id):
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
        r = requests.post(url, post_data)
        page_json = json.loads(r.text)
        if page_json['status'] == 'fail':
            return False
        else:
            return True

    def setDate(self, choose):
        if choose == '2':
            self.date = self.dates[1]
        else:
            self.date = self.dates[0]

    def getSeatId(self, room_id, seat_num):
        if len(seat_num) < 3:
            # 对座位号补零
            zero = (3 - len(seat_num)) * '0'
            seat_num = zero + seat_num
        url = 'http://seat.ujn.edu.cn/rest/v2/room/layoutByDate/%s/%s/?token=%s' % (room_id, self.date, self.token)
        r = requests.get(url)
        page_json = json.loads(r.text)
        if page_json['status'] != 'success':
            return page_json['message']
        data = page_json['data']
        seats = [i for i in data['layout'].values() if i['type'] == 'seat']
        for seat in seats:
            if seat['name'] == seat_num:
                return seat['id']

    def checkIn(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/checkIn?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        return page_json['message']

    def stop(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/stop?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        return page_json['message']

    def getMaxTime(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/allowedHours?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        return r.text

    def getHistory(self):
        # 1是页数从1开始 10为每页显示个数
        url = 'http://seat.ujn.edu.cn/rest/v2/history/1/10?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        res = page_json['data']['reservations']
        for re in res:
            for k in re:
                if re[k] is None:
                    continue
                elif isinstance(re[k], int):
                    re[k] = str(re[k])
                print k + ' : ' + re[k]

    def cancelRes(self):
        page_json = self.getHistory()
        res = page_json['data']['reservations']
        reserve = [i for i in res if i['stat'] == 'RESERVE']
        if len(reserve) == 0:
            return '没有预约的座位'
        resid = reserve[0]['id']
        url = 'http://seat.ujn.edu.cn/rest/v2/cancel/%s?token=%s' % (resid, self.token)
        r = requests.get(url)
        page_json = json.loads(r.text)
        return page_json['status']


def hackBook(room_id, seat_num, start_time, end_time, resDate):
    with open('can_use.txt', 'r') as f:
        lines = f.readlines()
    spent = int(end_time) - int(start_time)
    res_time = range(int(start_time), int(end_time))
    # print res_time
    flag = 1
    # 验证账号是否可用
    while flag < 2:
        flag += 1
        random_lines = random.sample(lines, spent)
        print random_lines
        i = 0
        while i < spent:
            line = random_lines[i]
            ap = line[:-1]
            t = res_time[i]
            i += 1
            try:
                p = PersonLib(ap)
                p.setDate(resDate)
                seat_id = p.getSeatId(room_id, seat_num)
                result = p.freeBook(t, t+1, seat_id)
            except TypeError:
                break
        else:
            break
    else:
        text = '无法登录'
        return text
    return '成功'


def menu():
    menu = '''
1. 快速预约
2. 自选座位
3. 结束使用
4. 签到
5. 查看楼层信息
6. 取消预约
7. 查看历史
9. 退出登录
0. 退出程序

请输入编号
    '''
    return menu

if __name__ == '__main__':
    need_login = True
    while True:
        while need_login:
            try:
                # ac = raw_input('账号')
                # pw = raw_input('密码')
                # std = PersonLib(ac, pw)
                std = PersonLib()
                need_login = False
            except TypeError, e:
                print e

        if not std.checkToken():
            print 'token error, 请重新登录'
            need_login = True
            continue

        a = raw_input(menu())
        if a == '0':
            break
        elif a == '9':
            need_login = True
        elif a == '1':
            hour = raw_input('预约时长:')
            std.quickBook(hour)
        elif a == '2':
            std.getSeat()
        elif a == '3':
            std.stop()
        elif a == '4':
            print std.checkIn()
        elif a == '5':
            print std.getBuildingsInfo()
        elif a == '6':
            std.cancelRes()
        elif a == '7':
            std.getHistory()
        elif a == '8':
            hackBook('19', '307', 7, 8, '2')
        else:
            print '输入错误, 请重新输入'
