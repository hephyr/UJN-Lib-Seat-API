#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import codecs
import random

from __init__ import *


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


def json_file(filename='seat.json'):
    with open(filename, 'r') as f:
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
        if user['id'] in [i['id'] for i in p.getUsingReservations()]:
            final_users.append(user)
    with codecs.open('using.json', 'w', 'utf-8') as f:
        json.dump(final_users, f, ensure_ascii=False, indent=4)


def reserve(t, date):
    seats = json_file()
    for seat in seats:
        p = randomLogin()
        if date != 1:
            p.setDate('2')
        option = p.book(t[0], t[1], seat['room_id'], seat['seat_num'])
        if option:
            writeToUsing(p)


def long_reserve(t, date):
    seats = json_file('new_seat.json')
    for seat in seats:
        if seat.get('username'):
            p = ujnlib(seat['username'], seat['password'])
        else:
            p = randomLogin()
        if date != 1:
            p.setDate('2')
        option = p.book(t[0], t[1], seat['room_id'], seat['seat_num'])
        if option:
            writeToUsing(p)


def res_main():
    times = [(8, 12), (12, 16), (16, 20)]
    for t in times:
        reserve(t, 2)
    long_reserve((8, 22), 2)
    cleanUsing()

if __name__ == '__main__':
    res_main()