#!/usr/bin/env Python
# -*- coding: utf-8 -*-
import socket

from ujnlib import *
from conf import *


def getUsingList():
    if SERVER:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVER, PORT))
        data = s.recv(8192).decode('utf-8')
        s.close()
        return data.split()
    else:
        with open('using.txt', 'r') as f:
            using_list = f.readlines()
        return [i[:-1] for i in using_list]


def checkIn():
    using_list = getUsingList()
    for username in using_list:
        p = ujnlib(username)
        if p.checkIn().status == 'success':
            print(p.getHistory().data.reservations[0].loc)
            print(p.getHistory().data.reservations[0].begin)


def main():
    checkIn()


if __name__ == '__main__':
    main()
