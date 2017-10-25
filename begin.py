#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import requests
import logging

from ujnlib import *
from reserve_seat import *

logging.basicConfig(filename='logger.log', level=logging.WARNING)

p = randomLogin()

while len(p.getDatetime()) == 1:
    time.sleep(30)
logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
times = [(8, 12), (12, 16), (16, 20)]
for t in times:
    reserve(t, 2)
cleanUsing()