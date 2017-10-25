#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
import codecs
from functools import wraps

from flask import Flask, request, current_app, jsonify

from ujnlib import *
app = Flask(__name__)


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function


def getUsername():
    with codecs.open('using.json', 'r', 'utf-8') as f:
        using_list = json.load(f)
    hour = int(time.strftime("%H"))
    date = time.strftime("%Y-%-m-%-d")
    return [{'username': i['username'], 'password': i['password']} for i in using_list if i['date'] == date and (int(i['begin'][:2]) == hour or int(i['begin'][:2]) == hour+1)]


def getToken():
    users = getUsername()
    tokens = []
    for user in users:
        p = ujnlib(user['username'], user['password'])
        tokens.append(p.token)
    return tokens


@app.route('/username')
@jsonp
def username():
    global count
    return jsonify(getUsername())


@app.route('/token')
@jsonp
def token():
    return jsonify(getToken())


@app.route('/res', methods=['POST'])
@jsonp
def reservation():
    room_id = request.form['room_id']
    seat_num = request.form['seat_num']


@app.route('/look')
@jsonp
def look():
    with open('using.json', 'r') as f:
        using_list = json.load(f)
    return jsonify(using_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
