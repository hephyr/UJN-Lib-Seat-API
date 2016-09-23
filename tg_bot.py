# -*- coding: utf-8 -*-

import telegram
import telegram.ext

import GetSeat

def getToken():
    with open('bot_token.txt', 'r') as f:
        TOKEN = f.readline()
    return TOKEN

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="输入账号")
    bot.sendMessage(chat_id=update.message.chat_id, text="输入密码")

if __name__ == '__main__':
    token = getToken()
    updater = telegram.ext.Updater(token=token)
    dispatcher = updater.dispatcher
    start_handler = telegram.ext.commandhandler.CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()