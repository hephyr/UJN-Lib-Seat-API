#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from scapy.all import *

def sendPca():
    pcare = PcapReader('./temp.pcap')
    for p in rd:
        np = p.payload
        np[IP].src = '172.16.219.219'
        del np[IP].chksum
        send(p)
def main():
    f = open('./p.pcap', 'r')
    lines = f.readlines()
    f.close()
    lines[1] = lines[1].replace('value', argv[1])
    f = open('./temp.pcap', 'w')
    for i in lines:
        f.write(i)
    f.close()
    sendPca()

if __name__ == '__main__':
    main()
