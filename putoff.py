#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import requests
from ujnlib import *
from reserve_seat import *

def getUsername():
    with open('using.json', 'r') as f:
        using_list = json.load(f)
    hour = int(time.strftime("%H"))
    date = time.strftime("%Y-%-m-%-d")
    return [i for i in using_list if i['date'] == date and (i['begin'][:2] == str(hour+1))]


def cancel():
    users = getUsername()
    begin = 1
    end = 1
    for user in users:
        p = ujnlib(user['username'])
        history = p.getHistory()
        res_id = history.data.reservations[0].id
        p.cancelRes(res_id)
        begin = int(user['begin'][:2]) + 1
        end = int(user['end'][:2])
    return (begin, end)


if __name__ == '__main__':
    t = cancel()
    if t[0] != t[1]:
        reserve(t, 1)
    cleanUsing()
