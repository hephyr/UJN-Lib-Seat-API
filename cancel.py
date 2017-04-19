#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import codecs

from ujnlib import *


def cleanUsing():
    with codecs.open('using.json', 'r', 'utf-8') as f:
        using_list = json.load(f)
    final_users = []
    for user in using_list:
        p = ujnlib(user['username'])
        if p.isInUse():
            final_users.append(user)
    with codecs.open('using.json', 'w', 'utf-8') as f:
        json.dump(final_users, f, ensure_ascii=False, indent=4)


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
    cleanUsing()


if __name__ == '__main__':
    main()
