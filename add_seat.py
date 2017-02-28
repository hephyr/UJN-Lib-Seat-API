#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ujnlib import *


def main():
    lib = ujnlib()
    print(lib.getBuildingsInfo())
    room_id = raw_input('阅览室id:')
    seat_num = raw_input('座位号:')
    seat_id = lib.getSeatId(room_id, seat_num)
    with open('seat.txt', 'a') as f:
        f.write(str(seat_id) + '\n')


if __name__ == '__main__':
    main()
