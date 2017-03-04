#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json

from flask import Flask

from ujnlib import *
app = Flask(__name__)


def getUsername():
    with open('using.json', 'r') as f:
        using_list = json.load(f)
    hour = int(time.strftime("%H"))
    return [i['username'] for i in using_list if i['begin'] == hour or i['begin'] == hour + 1]


def getToken():
    users = getUsername()
    tokens = []
    for user in users:
        p = ujnlib(user)
        tokens.append(p.token)
    return tokens


@app.route('/username')
def username():
    return json.dumps(getUsername())


@app.route('/token')
def token():
    return json.dumps(getToken())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
