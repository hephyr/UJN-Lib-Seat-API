#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import requests

from api import *


class ujnlib(UJNLibApi):
    def getBuildingsInfo(self):
        # 获取楼层信息
        info = self.building()
        if info.status == 'success':
            data = ''
            for value in info.data:
                data += 'id:' + str(value.roomId) + value.room
                data += u' 楼层:' + str(value.floor)
                data += u' 剩余:' + str(value.free) + '\n'
            return data
        else:
            return info.message

    def getBuildingsList(self):
        # return a list contain tuple for web
        info = self.building()
        building_list = []
        for value in info.data:
            building_list.append(
                            (str(value.roomId),
                             str(value.floor) + u'楼' + value.room))
        return building_list

    def getSeatTime(self, seat_id):
        # return text for human
        info = self.getSeatStartTime(seat_id)
        text = u'可开始时间\n'
        for i in info.data.startTimes:
            text += i.value + u'\n'
        return text

    def getSeatStartTimeList(self, seat_id):
        # return a list contain tuple for web
        info = self.getSeatStartTime()
        time_list = []
        for i in info.data.startTimes:
            time_list.append((i.id, i.value))
        return time_list

    def getSeatInfo(self, room_id, seat_num, resDate):
        # 获取座位状态
        self.setDate(resDate)
        seat_id = self.getSeatId(room_id, seat_num)
        return self.getSeatTime(seat_id)

    def quick(self, hour, building='2'):
        # 快速预约
        info = self.quickBook(hour, building)
        data = u''
        if info.status != 'success':
            return info.message
        else:
            data += u'日期: ' + info.data.reservation.onDate + '/n'
            data += u'开始时间: ' + info.data.reservation.begin + '/n'
            data += u'结束时间: ', info.data.reservation.end + '/n'
            data += u'地点: ', info.data.reservation.location + '/n'
            return data + info.message

    def free(self, start_time, end_time, seat_id):
        # 预约座位
        info = self.freeBook(start_time, end_time, seat_id)
        if info.status == 'fail':
            return False
        else:
            return True

    def getSeatId(self, room_id, seat_num):
        # 获取座位id
        if len(seat_num) < 3:
            # 对座位号补零
            zero = (3 - len(seat_num)) * '0'
            seat_num = zero + seat_num
        info = self.layoutByDate(room_id)
        if info.status != 'success':
            return info.message
        data = info.data
        seats = [i for i in data.layout.values() if i.type == 'seat']
        for seat in seats:
            if seat.name == seat_num:
                return seat.id

    def isInUse(self):
        # 检测账号是否正在使用
        info = self.getHistory()
        res = info.data.reservations
        reserve = [i for i in res if i.stat == 'CHECK_IN' or i.stat == 'RESERVE']
        return True if reserve else False


def hackBook(room_id, seat_num, start_time, end_time, resDate):
    # 黑科技
    with open('can_use.txt', 'r') as f:
        lines = f.readlines()
    spent = int(end_time) - int(start_time)
    res_time = range(int(start_time), int(end_time))
    random_lines = random.sample(lines, spent*3)
    i = 0
    text = ''
    while i < len(random_lines):
        line = random_lines[i]
        ap = line[:-1]
        t = res_time[0]
        try:
            p = ujnlib(ap)
            if p.isInUse():
                continue
            else:
                with open('used.txt', 'a') as f:
                    f.write(line)
        except TypeError:
            continue
        finally:
            i += 1
        res_time = res_time[1:]
        p.setDate(resDate)
        seat_id = p.getSeatId(room_id, seat_num)
        result = p.freeBook(t, t+1, seat_id)
        if result:
            text += str(t) + '-' + str(t+1) + ':预约成功\n'
        else:
            text += str(t) + '-' + str(t+1) + ':预约失败\n'
        if len(res_time) == 0:
            break
    else:
        return 'Something wrong'

    return text


def menu():
    menu = '''
1. 查看楼层信息
2. 查看座位信息
3. 预约
0. 退出程序

请输入编号
    '''
    return menu


def main():
    pass


if __name__ == '__main__':
    while True:
        std = ujnlib()
        if not std.checkToken():
            print('token error, 请重新登录')
            continue

        a = raw_input(menu())
        if a == '0':
            break
        elif a == '1':
            print(std.getBuildingsInfo())
        elif a == '2':
            room_id = raw_input('阅览室id:')
            seat_num = raw_input('座位号:')
            resDate = raw_input('是否为明天 ?(Y/n)')
            print(std.getSeatInfo(room_id, seat_num, resDate))
        elif a == '3':
            room_id = raw_input('阅览室id:')
            seat_num = raw_input('座位号:')
            start_time = raw_input('请输入开始时间(24进制):')
            end_time = raw_input('请输入结束时间(24进制):')
            resDate = raw_input('是否为明天 ?(Y/n)')
            print(hackBook(room_id, seat_num, start_time, end_time, resDate))
        else:
            print('输入错误, 请重新输入')
