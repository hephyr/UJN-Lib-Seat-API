#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
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


def reserve(date):
    seats = json_file()
    for seat in seats:
        for ti in seat['times']:
            if ti.get('username'):
                try:
                    p = ujnlib(ti['username'], ti['password'])
                except:
                    p = randomLogin()
            else:
                p = randomLogin()
            if date != 1:
                p.setDate('2')
            option = p.book(ti['begin'], ti['end'], seat['room_id'], seat['seat_num'])
            if option:
                writeToUsing(p)

def reres():
    seats = json_file()
    h_now = int(time.strftime("%H"))
    end = 1
    for seat in seats:
        for ti in seat['times']:
            if h_now in range(int(ti['begin']), int(ti['end'])):
                if ti.get('username'):
                    try:
                        p = ujnlib(ti['username'], ti['password'])
                    except:
                        p = randomLogin()
                else:
                    p = randomLogin()
                option = p.book(h_now+1, ti['end'], seat['room_id'], seat['seat_num'])
                end = ti['end']
                if option:
                    writeToUsing(p)
    return (h_now, end)


def res_main():
    reserve(2)
    cleanUsing()

if __name__ == '__main__':
    res_main()