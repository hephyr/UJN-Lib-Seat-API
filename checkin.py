#!/usr/bin/env Python
# -*- coding: utf-8 -*-
import socket

from ujnlib import *


def getUsingList():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('202.194.67.74', 23333))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data.split()


def checkIn():
    using_list = getUsingList()
    for username in using_list:
        p = ujnlib(username)
        p.checkIn()


def main():
    checkIn()


if __name__ == '__main__':
    main()
