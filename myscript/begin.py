#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import requests
import logging

from __init__ import *
from reserve_seat import *

logging.basicConfig(filename='logger.log', level=logging.WARNING)

p = randomLogin()

while len(p.getDatetime()) == 1:
    time.sleep(30)
logging.warn(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
res_main()