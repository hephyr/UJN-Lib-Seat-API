#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import codecs

from __init__ import *
from reserve_seat import *

def cancel(p, id):
    p.cancelRes(id)


def main():
    with open('using.json', 'r') as f:
        using_list = json.load(f)
    for user in using_list:
        p = ujnlib(user['username'], user['password'])
        cancel(p, user['id'])
    cleanUsing()

    with open('seat.json', 'r') as f:
        seats = json.load(f)
    for seat in seats:
        for ti in seat['times']:
            if ti.get('username'):
                try:
                    p = ujnlib(ti['username'], ti['password'])
                    use = p.getUsingReservations()
                    for i in use:
                        p.cancelRes(i['id'])
                except:
                    pass

if __name__ == '__main__':
    main()
