#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import math
import json
import random

import requests
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler

from GetSeat import *

updater = Updater(token='247176950:AAFaJefszLKQlqy1YpOXTA60lT8ZjZ8eQsw')
dispatcher = updater.dispatcher


def getUrl(text):
    text = text.strip()
    grade = text[:4]
    url = 'http://iplat.ujn.edu.cn/photo/%s/%s.jpg' % (grade, text)
    r = requests.get(url)
    if r.status_code == 200:
        return str(url)
    else:
        return False


def echo(bot, update):
    text = update.message.text
    url = getUrl(text)
    if url is False:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id, text='Error')
    else:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=update.message.chat_id, photo=url)


def cmdPhoto(bot, update, args):
    url = getUrl(args[0])
    if url is False:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id, text='Error')
    else:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=update.message.chat_id, photo=url)


def randomPhoto(bot, update):
    base_url = 'http://gank.io/api/random/data/福利/1'
    r = requests.get(base_url)
    data = json.loads(r.text)
    img_src = data['results'][0]['url']
    url = img_src.encode()
    r = requests.get(url, stream=True)
    img = r.raw.read()
    f = open('photo.jpg', 'wb')
    f.write(img)
    f.close()
    try:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=update.message.chat_id,
                      photo=open('photo.jpg', 'rb'))
        os.remove('photo.jpg')
    except BaseException, e:
        bot.sendChatAction(chat_id=update.message.chat_id,
                           action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id, text=str(e))
        bot.sendMessage(chat_id=update.message.chat_id, text=url)


def cmdRed(bot, update):
    base_url = 'http://7xqh4i.com1.z0.glb.clouddn.com/pic%s.jpg'
    i = random.randint(0, 330)
    url = base_url % str(i)
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=telegram.ChatAction.UPLOAD_PHOTO)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=url)


def cmdGetBuildingInfo(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=telegram.ChatAction.TYPING)
    person = PersonLib()
    text = person.getBuildingsInfo()
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def cmdGetSeatInfo(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=telegram.ChatAction.TYPING)
    person = PersonLib()
    room_id = args[0]
    seat_num = args[1]
    resDate = '1'
    if len(args) == 3 and args[2] == '2':
        resDate = '2'
    text = person.getSeatInfo(room_id, seat_num, resDate)
    bot.sendMessage(chat_id=update.message.chat_id, text=text)


def cmdGetSeat(bot, update, args):
    bot.sendChatAction(chat_id=update.message.chat_id,
                       action=telegram.ChatAction.TYPING)
    room_id = args[0]
    seat_num = args[1]
    start_time = args[2]
    end_time = args[3]
    resDate = '1'
    if len(args == 5) and args[4] == '2':
        resDate = '2'
    text = hackBook(room_id, seat_num, start_time, end_time, resDate)
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

echo_handler = MessageHandler([Filters.text,
                               Filters.photo,
                               Filters.status_update],
                              echo)
photo_handler = CommandHandler('num', cmdPhoto,  pass_args=True)
girl_random_handler = CommandHandler('girl', randomPhoto)
red_handler = CommandHandler('red', cmdRed)
building_info_handler = CommandHandler('building', cmdGetBuildingInfo)
seat_time_handler = CommandHandler('seat', cmdGetSeatInfo, pass_args=True)
get_seat_handler = CommandHandler('get', cmdGetSeat, pass_args=True)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(girl_random_handler)
dispatcher.add_handler(red_handler)
dispatcher.add_handler(building_info_handler)
dispatcher.add_handler(seat_time_handler)
dispatcher.add_handler(get_seat_handler)
updater.start_polling()
