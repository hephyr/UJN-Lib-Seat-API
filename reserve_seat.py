#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from ujnlib import *


def randomLogin():
    while True:
        with open('can_use.txt', 'r') as f:
            lines = f.readlines()
        i = random.randint(0, len(lines) - 1)
        username = lines[i]
        p = ujnlib(username[:-1])
        if not p.isInUse():
            return p


def getSeatList():
    with open('seat.txt', 'r') as f:
        seats_str = f.readlines()
    seats = []
    for seat_json in seats_str:
        data = json.loads(seat_json)
        p = ujnlib()
        seat = p.getSeatId(data['room_id'], data['seat_num'])
        seats.append(seat)
    return seats


def writeToUsing(username):
    with open('using.txt', 'a') as f:
        f.write(str(username) + '\n')


def cleanUsing():
    with open('using.txt', 'r') as f:
        using_list = f.readlines()
    users = [i[:-1] for i in using_list]
    final_users = []
    for user in users:
        p = ujnlib(user)
        if p.isInUse():
            final_users.append(user)
    with open('using.txt', 'w') as f:
        for user in final_users:
            f.write(user + '\n')


def reserve(t):
    seats = getSeatList()
    for seat in seats:
        p = randomLogin()
        p.setDate('2')
        option = p.free(t[0], t[1], seat)
        if option:
            writeToUsing(p.ac)


def main():
    times = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20)]
    for t in times:
        reserve(t)
    cleanUsing()


if __name__ == '__main__':
    main()
