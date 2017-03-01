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
        data = json.loads(seat)
        p = ujnlib()
        seat = p.getSeatId(data['room_id'], data['seat_id'])
        seats.append(seat)
    return seats


def writeToUsing(username):
    with open('using.txt', 'a') as f:
        f.write(str(username) + '\n')


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


if __name__ == '__main__':
    main()
