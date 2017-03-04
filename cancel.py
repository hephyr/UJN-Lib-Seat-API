#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from ujnlib import *


def cancel(p):
    history = p.getHistory()
    res_id = history.data.reservations[0].id
    p.cancelRes(res_id)


def main():
    with open('using.json', 'r') as f:
        using_list = json.load(f)
    for user in using_list:
        p = ujnlib(user['username'])
        cancel(p)


if __name__ == '__main__':
    main()
