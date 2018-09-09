#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
            logger.error('%s: %s' % (self.ac, info.message))
            return False
        else:
            logger.info('%s%s' % (self.ac, '预约成功'))
            return True

    def book(self, start_time, end_time, room_id, seat_num):
        # 预约座位
        logger.info('%s%s %s-%s' % (self.ac, ': 开始预约', start_time, end_time))
        seat_id = self.getSeatId(room_id, seat_num)
        return self.free(start_time, end_time, seat_id)

    def getSeatId(self, room_id, seat_num):
        # 获取座位id
        seat_num = str(seat_num)
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

    def getUsingReservations(self):
        info = self.getHistory()
        res = info.data.reservations
        return [i for i in res if i.stat == 'CHECK_IN' or i.stat == 'RESERVE']

    def setDateToday(self):
        self.setDate('1')

    def setDateTomorrow(self):
        self.setDate('2')
