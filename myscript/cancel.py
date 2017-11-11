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


if __name__ == '__main__':
    main()
