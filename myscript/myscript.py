#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


def reserve_one(date, seat, ti):
    try:
        p = ujnlib(ti['username'], ti['password'])
        if date != 1:
            p.setDateTomorrow()
        option = p.book(ti['begin'], ti['end'], seat['room_id'], seat['seat_num'])
    except LoginException as e:
        logging.error(e.err)


def reserve_all(date):
    print "Starting at:", time.ctime()
    threads = []

    seats = json_file()
    for seat in seats:
        for ti in seat['times']:
            t = threading.Thread(target=reserve_one, args=(date, seat, ti))
            threads.append(t)
    n_threads = range(len(threads))

    for i in n_threads:
        threads[i].start()
    for i in n_threads:
        threads[i].join()

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
