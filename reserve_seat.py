#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import random

from ujnlib import *


def randomLogin():
    while True:
        with open('can_use.txt', 'r') as f:
            lines = f.readlines()
        i = random.randint(0, len(lines) - 1)
        username = lines[i]
        try:
            p = ujnlib(username[:-1])
            if not p.isInUse():
                return p
        except Exception:
            pass


def getSeatList():
    with open('seat.json', 'r') as f:
        seats_json = json.load(f)
    seats = []
    for data in seats_json:
        p = ujnlib()
        seat = p.getSeatId(data['room_id'], data['seat_num'])
        seats.append(seat)
    return seats


def writeToUsing(username, begin, end):
    with open('using.json', 'r') as f:
        using = json.load(f)
    data = {'username': username,
            'begin': begin,
            'end': end}
    using.append(data)
    with open('using.json', 'w') as f:
        json.dump(using, f, indent=4)


def cleanUsing():
    with open('using.json', 'r') as f:
        using_list = json.load(f)
    final_users = []
    for user in using_list:
        p = ujnlib(user['username'])
        if p.isInUse():
            final_users.append(user)
    with open('using.json', 'w') as f:
        json.dump(final_users, f, indent=4)


def reserve(t):
    seats = getSeatList()
    for seat in seats:
        p = randomLogin()
        p.setDate('2')
        option = p.free(t[0], t[1], seat)
        if option:
            writeToUsing(p.ac, t[0], t[1])


def main():
    times = [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)]
    for t in times:
        reserve(t)
    cleanUsing()


if __name__ == '__main__':
    main()
