from config import *
from datetime import datetime
from telebot import types
import telebot
import os
import requests
import time

class NotificationBot():
    def __init__(self):
        self.bot = telebot.TeleBot(os.getenv('NotificationCrypto'))

    def get_data(self, message, symbol):
        try:
            response = requests.get(site + symbol).json()

            answer = "Date: " + datetime.now().strftime("%Y-%m-%d") + "\n" + \
                     "Time: " + datetime.now().strftime("%H:%M:%S") + "\n" + \
                     "Price: " + str(float(response["price"]))

            self.bot.send_message(message.chat.id, answer)
        except Exception as ex:
            print(f"***Exception: {ex}***")

    def bot_message(self):
        @self.bot.message_handler(commands=["start"])
        def start_message(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("BTC"),
                       types.KeyboardButton("ETH"),
                       types.KeyboardButton("BNB"))

            self.bot.send_message(message.chat.id, "Hello!\nI am displaying crypto prices!\nYou can choose crypto!",
                             reply_markup=markup)

        @self.bot.message_handler(content_types=["text"])
        def send_text(message):
            try:
                if message.text.strip().lower() == "btc":
                    t0 = time.time()
                    self.get_data(message, symbol_btc)
                    print(time.time()-t0)
                elif message.text.strip().lower() == "eth":
                    t0 = time.time()
                    self.get_data(message, symbol_eth)
                    print(time.time()-t0)
                elif message.text.strip().lower() == "bnb":
                    t0 = time.time()
                    self.get_data(message, symbol_bnb)
                    print(time.time()-t0)
                else:
                    self.bot.send_message(message.chat.id, "Please, text [price] or click on button!")
            except Exception as ex:
                print(f"***Exception: {ex}***")

        self.bot.infinity_polling()

if __name__ == '__main__':
    print("Program started!")
    BOT = NotificationBot()
    BOT.bot_message()
    print("***Program Never Ended!!!***\nBut...\n ):If you see this message, it was ended:(")
