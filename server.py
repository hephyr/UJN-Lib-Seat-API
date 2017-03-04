#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
import socket
import threading

from conf import *


def tcplink(sock, addr):
    with open('using.json', 'r') as f:
        using_json = json.load(f)
        hour = int(time.strftime("%H"))
        using_list = [i['username'] for i in using_json if i['begin'] == hour or i['begin'] == hour + 1]
    s = ' '
    users = s.join(using_list)
    sock.send(users)
    sock.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER, PORT))
    s.listen(5)
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

if __name__ == '__main__':
    main()
