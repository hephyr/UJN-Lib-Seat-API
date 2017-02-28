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
        seats = f.readlines()
        return [seat[:-1] for seat in seats]


def writeToUsing(username):
    with open('using.txt', 'a') as f:
        f.write(str(username) + '\n')


def reserve(t):
    seats = getSeatList()
    for seat in seats:
        p = randomLogin()
        # p.setDate('2')
        p.freeBook(t[0], t[1], seat)
        writeToUsing(p.ac)


def main():
    # times = [(8, 12), (12, 16), (16, 20)]
    times = [(16, 17)]
    for t in times:
        reserve(t)


if __name__ == '__main__':
    main()
