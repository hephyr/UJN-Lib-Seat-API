#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time
import codecs
import random

from __init__ import *

def json_file(filename='seat.json'):
    with open(filename, 'r') as f:
        seats_json = json.load(f)
    return seats_json

def reserve(date):
    seats = json_file()
    for seat in seats:
        for ti in seat['times']:
            p = ujnlib(ti['username'], ti['password'])
            if date != 1:
                p.setDateTomorrow()
            option = p.book(ti['begin'], ti['end'], seat['room_id'], seat['seat_num'])

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
    # main
    pass