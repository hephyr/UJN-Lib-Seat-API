#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from ujnlib import *


def main():
    lib = ujnlib()
    print(lib.getBuildingsInfo())
    room_id = raw_input('阅览室id:')
    seat_num = raw_input('座位号:')
    note = raw_input('备注:')
    data = {'room_id': room_id,
            'seat_num': seat_num,
            'note': note}
    json_str = json.dumps(data)
    with open('seat.txt', 'a') as f:
        f.write(json_str + '\n')


if __name__ == '__main__':
    main()
