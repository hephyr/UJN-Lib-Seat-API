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
    return [i['username'] for i in using_list if i['date'] == date and (i['begin'][:2] == str(hour+1))]


def cancel():
    users = getUsername()
    for user in users:
        p = ujnlib(user)
        history = p.getHistory()
        res_id = history.data.reservations[0].id
        p.cancelRes(res_id)
    begin = int(history.data.reservations[0].begin[:2]) + 1
    end = int(history.data.reservations[0].end[:2])
    return (begin, end)


if __name__ == '__main__':
    t = cancel()
    if t[0] != t[1]:
        reserve(t)
        cleanUsing()
