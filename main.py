# -*- coding: utf-8 -*-

import time
from bot import Sevabot

from flask import Flask, request
import settings
from hashlib import md5


server = Flask(__name__)
sevabot = Sevabot()


def main():

    print("Starting bot")

    server.run()

    #fuck cron stuff for now
    #interval = 1
    # while(True):
    #     time.sleep(interval)
    #     sevabot.runCron(interval)


@server.route("/cmd/<string:cmd>")
def command(cmd):
    try:
        return sevabot.runCmd(cmd).replace("\n", "<br />")
    except Exception as e:
        return str(e)


@server.route("/msg/", methods=['POST'])
def message():
    try:
        if request.method == 'POST':
            if ('chat' in request.form and
               'msg' in request.form and
               'md5' in request.form):

                chat = request.form['chat']
                msg = request.form['msg']
                m = request.form['md5']

                mcheck = md5(chat + msg + settings.SHARED_SECRET).hexdigest()
                if mcheck == m:
                    sevabot.sendMsg(chat, msg)
                else:
                    return "No can do %s\n" % (mcheck)
        return "Message sent"
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    main()