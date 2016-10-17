#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import datetime
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

    def getBuildingsInfo(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/room/stats2/2?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        if page_json['status'] == 'success':
            for value in page_json['data']:
                print 'id:', value['roomId'], value['room'],\
                    '楼层:', value['floor'], ' 剩余:', value['free']
            return page_json['data']
        else:
            return page_json['message']

    def getSeatInfo(self, seat, date):
        to21clock = False

        begtimeurl = 'http://seat.ujn.edu.cn/rest/v2/startTimesForSeat/%s/%s?token=%s' % (seat, date, self.token)
        begpage = requests.get(begtimeurl)
        page_json = json.loads(begpage.text)
        startlist = page_json['data']['startTimes']

        hour = '480'

        if date == datetime.date.today():
            hour = (datetime.datetime.today() + datetime.timedelta(hours=1)).hour
            hour = str(hour * 60)

        endtime = 1260
        if startlist:
            try:
                time = startlist[1]['id']
            except BaseException:
                return False

            if time == hour:
                for data in startlist[:0:-1]:
                    time = data['id']
                    if time != str(endtime):
                        break
                    else:
                        endtime -= 60
                else:
                    to21clock = True
        else:
            print '○',
        return to21clock

    def layoutByDate(self, roomId, date):
        url = 'http://seat.ujn.edu.cn/rest/v2/room/layoutByDate/%s/%s/?token=%s' % (roomId, date, self.token)
        r = requests.get(url)
        page_json = json.loads(r.text)
        if page_json['status'] != 'success':
            return False
        data = page_json['data']
        print data['name']
        layout = data['layout']

        l = [layout[x] for x in layout if layout[x]['type'] == 'seat']
        l = sorted(l, key=lambda x: x['name'])
        d = {}
        for i in l:
            print '座位号:', i['name'], '是否可预约到21点:',
            d[i['name']] = i['id']
            if self.getSeatInfo(i['id'], date):
                print '✓'
            else:
                print ''

        return d

    def quickBook(self):
        hour = raw_input('预约时长:')
        post_data = {
            "token": self.token,
            "building": "2",
            "hour": hour
        }
        url = 'http://seat.ujn.edu.cn/rest/v2/quickBook'
        r = requests.post(url, post_data)
        page_json = json.loads(r.text)
        if page_json['status'] != 'success':
            print '预约失败', page_json['message']
        else:
            print '日期: ', page_json['data']['reservation']['onDate']
            print '开始时间: ', page_json['data']['reservation']['begin']
            print '结束时间: ', page_json['data']['reservation']['end']
            print '地点: ', page_json['data']['reservation']['location']
            return page_json['message']

    def getSeat(self):
        date = datetime.date.today()
        strdate = date.strftime('%Y-%m-%d')
        self.getBuildingsInfo()
        roomId = raw_input('room id :')
        while True:
            print '1. 今天'
            print '2. 明天'
            a = raw_input()
            if a == '1':
                break
            elif a == '2':
                date += datetime.timedelta(days=1)
                strdate = date.strftime('%Y-%m-%d')
                break
            else:
                print '输入错误'
        seat_dict = self.layoutByDate(roomId, date)
        while True:
            seat = raw_input('输入座位号:')
            if len(seat) < 3:
                zero = (3 - len(seat)) * '0'
                seat = zero + seat
            if seat not in seat_dict.keys():
                print '座位号错误'
            else:
                break
        while True:
            startTime = int(raw_input('输入开始时间 (7:00输入7    20:00输入20   最晚22)'))

            if date == datetime.date.today():
                hour = datetime.datetime.today()
                hour = int(hour.strftime('%H'))
                if startTime < hour or hour > 22:
                    print '输入错误'
                else:
                    break
            else:
                if startTime < 7 or startTime > 22:
                    print '输入错误'
                else:
                    break

        startTime *= 60
        startTime = str(startTime)
        post_data = {
            'token': self.token,
            'startTime': startTime,
            'endTime': '1320',
            'seat': seat_dict[seat],
            'date': date
        }

        url = 'http://seat.ujn.edu.cn/rest/v2/freeBook'
        r = requests.post(url, post_data)
        page_json = json.loads(r.text)
        if page_json['status'] != 'success':
            print page_json['message']
        else:
            print '预约成功'

    def checkIn(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/checkIn?token=%s' % self.token
        r = requests.get(url)
        page_json = json.loads(r.text)
        print page_json
        return page_json['message']

    def stop(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/stop?token=%s' % self.token
        r = requests.get(url)
        print r.text

    def getMaxTime(self):
        url = 'http://seat.ujn.edu.cn/rest/v2/allowedHours?token=%s' % self.token
        r = requests.get(url)
        page = r.text
        print page

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
                ac = raw_input('账号')
                pw = raw_input('密码')
                std = PersonLib(ac, pw)
                # std = PersonLib()
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
            std.quickBook()
        elif a == '2':
            std.getSeat()
        elif a == '3':
            std.stop()
        elif a == '4':
            std.checkIn()
        elif a == '5':
            std.getBuildingsInfo()
        elif a == '6':
            std.cancelRes()
        elif a == '7':
            std.getHistory()
        else:
            print '输入错误, 请重新输入'
