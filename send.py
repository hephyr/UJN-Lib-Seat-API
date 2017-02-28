#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scapy.all import *


def sendThePac(p, token):
    request = IP(dst='202.194.76.30', src='172.16.219.219') / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr




def main():
    pass


if __name__ == '__main__':
    main()
