#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import datetime
import json
import logging
import time
import threading

from __init__ import *
from libapi.login_exception import LoginException

units = Queue.Queue()


def json_file(filename='seat.json'):
    with open(filename, 'r') as f:
        seats_json = json.load(f)
    return seats_json


def login_one(is_tomorrow, ti, seat):
    try:
        p = ujnlib(ti['username'], ti['password'])
        if is_tomorrow != 1:
            p.setDateTomorrow()
        units.put((p, (seat['room_id'], seat['seat_num']), (ti['begin'], ti['end'])))
    except LoginException as exception:
        logging.error(exception.err)


def reserve_one(p, seat, ti):
    p.book(ti[0], ti[1], seat[0], seat[1])


# 多线程登录
def login_all(is_tomorrow, lists):
    threads_login = []
    for per in lists:
        for ti in per['times']:
            t = threading.Thread(target=login_one, args=(is_tomorrow, ti, per))
            threads_login.append(t)
    n_threads = range(len(threads_login))
    for i in n_threads:
        threads_login[i].start()
    for i in n_threads:
        threads_login[i].join()


def wait_to(target_time):
    logging.info("等待到达指定时间...")
    str_target = str(datetime.datetime.now().date()) + " " + target_time
    struct_time_target = time.strptime(str_target, "%Y-%m-%d %H:%M:%S")
    stamp_target = time.mktime(struct_time_target)
    stamp_now = time.time()
    stamp_interval = stamp_target - stamp_now
    if stamp_interval > 0:
        time.sleep(stamp_interval)


def reserve_all(is_tomorrow):
    logging.info("开始运行")
    # obj,seat,time的数目一一对应,三个list一样长
    objs, seats, times = [], [], []

    lists = json_file()
    login_all(is_tomorrow, lists)

    # 将登录所得结果集分开
    while not units.empty():
        unit = units.get()
        objs.append(unit[0])
        seats.append(unit[1])
        times.append(unit[2])
    wait_to("05:00:00")

    # 多线程预约
    threads_reserve = []
    for i in range(len(objs)):
        t = threading.Thread(target=reserve_one, args=(objs[i], seats[i], times[i]))
        threads_reserve.append(t)
    n_threads = range(len(threads_reserve))
    for i in n_threads:
        threads_reserve[i].start()
    for i in n_threads:
        threads_reserve[i].join()

    logging.info("结束")


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
