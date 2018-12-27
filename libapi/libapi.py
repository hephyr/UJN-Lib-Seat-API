#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import requests

from .leoapi import leoapi
from .utils import JsonDict


class libapi(leoapi):

    def dates(self):
        # 可预约日期列表
        resp = self.filters()
        return resp.data.dates
    
    def rooms(self):
        resp = self.filters()

        buildings =  resp.data.buildings
        d = {"buildings": [], "rooms": []}
        for building in buildings:
            d["buildings"].append({
                "buildingID": building[0],
                "buildingName": building[1]
            })

        rooms = resp.data.rooms
        for room in rooms:
            d["rooms"].append({
                "buildingID": room[2],
                "roomName": room[1],
                "roomID": room[0],
                "floor": room[3]
            })

        return JsonDict(d)

    def getSeatIDbyNum(self, room_id, seat_num):
        # 通过阅览室ID和座位号获得座位ID
        seat_num = str(seat_num)
        if len(seat_num) < 3:
            # 对座位号补零
            zero = (3 - len(seat_num)) * '0'
            seat_num = zero + seat_num
        info = self.layoutByDate(room_id, self.dates()[0])
        if info.status != 'success':
            raise Exception("阅览室ID或座位号错误")
        data = info.data
        seats = [i for i in data.layout.values() if i.type == 'seat']
        for seat in seats:
            if seat.name == seat_num:
                return seat.id
    
    def getRoomIDbyName(self, room_name):
        rooms = self.filters().data.rooms
        for room in rooms:
            if room[1] == room_name:
                return room[0]
    
    def getRoomNamebyID(self, room_id):
        rooms = self.filters().data.rooms
        for room in rooms:
            if int(room[0]) == int(room_id):
                return room[1]
    
    def seatInfo(self, room_id, seat_num):
        # 查看座位信息
        seat_id = self.getSeatIDbyNum(room_id, seat_num)
        d = {
                "roomName": self.getRoomNamebyID(room_id),
                "roomID": room_id,
                "seatNum": seat_num,
                "seatID": seat_id,
                "times": []
            }
        for date in self.dates():
            start = self.seatStartTime(seat_id, date)
            d["times"].append({
                "date": date,
                "startTimes": start.data.startTimes
            })
        return JsonDict(d)


    def book(self, start_time, end_time, room_id, seat_num, date):
        # 预约座位
        # date can be 'today' or 'tomorrow' or like '2012-03-04'
        if date == "today":
            date = self.dates()[0]
        elif date == "tomorrow":
            dates = self.dates()
            if len(dates) < 2:
                return JsonDict({"status": "fail", "message": "dates just have " + dates})
            else:
                date = dates[1]
        seat_id = self.getSeatIDbyNum(room_id, seat_num)
        return self.freeBook(start_time, end_time, seat_id, date)

    def isInUse(self):
        # 检测账号是否正在使用
        info = self.reservations()
        if info.data is None:
            return True
        else:
            return False
