#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import codecs
import random

from ujnlib import *


def randomLogin():
    while True:
        with open('new_use.txt', 'r') as f:
            lines = f.readlines()
        i = random.randint(0, len(lines) - 1)
        s = lines[i]
        username = s.split()[0]
        password = s.split()[1]
        try:
            p = ujnlib(username, password)
            if not p.isInUse():
                return p
        except Exception:
            pass


def getSeatList():
    with open('seat.json', 'r') as f:
        seats_json = json.load(f)
    return seats_json


def writeToUsing(p):
    with codecs.open('using.json', 'r') as f:
        using = json.load(f)
    history = p.getHistory()
    data = {'username': p.ac, 'password': p.pw}
    d = dict(data, **history.data.reservations[0])
    using.append(d)
    with codecs.open('using.json', 'w', 'utf-8') as f:
        json.dump(using, f, ensure_ascii=False, indent=4)


def cleanUsing():
    with codecs.open('using.json', 'r', 'utf-8') as f:
        using_list = json.load(f)
    final_users = []
    for user in using_list:
        p = ujnlib(user['username'], user['password'])
        if p.isInUse():
            final_users.append(user)
    with codecs.open('using.json', 'w', 'utf-8') as f:
        json.dump(final_users, f, ensure_ascii=False, indent=4)


def reserve(t, date):
    seats = getSeatList()
    for seat in seats:
        p = randomLogin()
        if date != 1:
            p.setDate('2')
        option = p.book(t[0], t[1], seat['room_id'], seat['seat_num'])
        if option:
            writeToUsing(p)


if __name__ == '__main__':
    times = [(10, 12), (12, 16), (16, 20)]
    for t in times:
        reserve(t, 2)
    cleanUsing()
