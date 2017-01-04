#!/usr/bin/env Python
# -*- coding: utf-8 -*-

from GetSeat import *

with open('used.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line[:-1]
    p = PersonLib(line)
    print(p.checkIn())
