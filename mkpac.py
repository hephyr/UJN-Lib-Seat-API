#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv


def main():
    f = open('./p.pcap', 'r')
    lines = f.readlines()
    f.close()
    lines[1] = lines[1].replace('value', argv[1])
    f = open('./temp.pcap', 'w')
    for i in lines:
        f.write(i)
    f.close()

if __name__ == '__main__':
    main()
