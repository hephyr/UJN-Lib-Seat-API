#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import logging
import time
import threading

from __init__ import *
from libapi.login_exception import LoginException


def json_file(filename='seat.json'):
    with open(filename, 'r') as f:
        seats_json = json.load(f)
    return seats_json


def login_one(date, ti, seat):
    try:
        p = ujnlib(ti['username'], ti['password'])
        if date != 1:
            p.setDateTomorrow()
        return p, (seat['room_id'], seat['seat_num']), (ti['begin'], ti['end'])

    except LoginException as exception:
        logging.error(exception.err)
        return None


def reserve_one(p, seat, ti):
    p.book(ti[0], ti[1], seat[0], seat[1])


def reserve_all(date):
    print "Starting at:", time.ctime()
    logging.info("开始")

    # unit,seat,time的数目一一对应,三个list一样长
    units = []
    seats = []
    times = []

    # 解析文件
    lists = json_file()

    # 登录
    for per in lists:
        for ti in per['times']:
            unit, seat, ti = login_one(date, ti, per)
            if unit is not None:
                units.append(unit)
                seats.append(seat)
                times.append(ti)

    logging.info("等待到达指定时间...")
    str_target = str(datetime.datetime.now().date()) + " 14:55:00"
    struct_time_target = time.strptime(str_target, "%Y-%m-%d %H:%M:%S")
    stamp_target = time.mktime(struct_time_target)
    stamp_now = time.time()
    stamp_interval = stamp_target - stamp_now
    if stamp_interval > 0:
        time.sleep(stamp_interval)

    # 多线程预约
    reserve_threads = []
    for i in range(len(units)):
        t = threading.Thread(target=reserve_one, args=(units[i], seats[i], times[i]))
        reserve_threads.append(t)
    n_threads = range(len(reserve_threads))
    for i in n_threads:
        reserve_threads[i].start()
    for i in n_threads:
        reserve_threads[i].join()

    logging.info("结束")
    print "All DONE at:", time.ctime()


def check_in():
    seats = json_file()
    hour = int(time.strftime("%H"))
    # date = time.strftime("%Y-%-m-%-d")
    accounts = []
    for seat in seats:
        for t in seat['times']:
            if t['begin'] == str(hour) or t['begin'] == str(hour + 1):
                p = ujnlib(t['username'], t['password'])
                p.checkIn()


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'c':
            check_in()
        elif sys.argv[1] == 'r':
            reserve_all(2)
    except IndexError as e:
        print("参数c:签到\n参数r:预约")
