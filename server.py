#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import threading


def tcplink(sock, addr):
    with open('using.txt', 'r') as f:
        using_list = [i[:-1] for i in f.readlines()]
    s = ' '
    users = s.join(using_list)
    sock.send(users)
    sock.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 23333))
    s.listen(5)
    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()

if __name__ == '__main__':
    main()
