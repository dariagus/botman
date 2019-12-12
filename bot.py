#!pip install pyTelegramBotAPI
import telebot

token = '986794089:AAEpR4ZdfO5EH2AVMirQRqzgd6Gka6fWmtQ'

bot = telebot.TeleBot(token)

import pytz
import json
import traceback
import re  
import requests 
  
URL = 'https://api.exchangeratesapi.io/latest?base=RUB'  
  
def load_exchange():  
    return json.loads(requests.get(URL).text) 

dict = load_exchange()

def get_exchange(curr): 
    return dict.get('rates', {}).get(curr)

bot = telebot.TeleBot(token, threaded = False)

    
@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'Здравствуйте! Я Botman, могу поделиться с вами валютными курсами RUB по отношению к USD, EUR, GBP \n' + 
'Если нужны валютные курсы по отношению к рублю, жми  /exchange.\n' + 
'А если нужна помощь, то /help.'  
  )
    

@bot.message_handler(commands=['exchange'])
def mychat(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('USD', callback_data = 'USD'))
    keyboard.row(telebot.types.InlineKeyboardButton('EUR', callback_data = 'EUR'))
    keyboard.row(telebot.types.InlineKeyboardButton('GBP', callback_data = 'GBP'))
    bot.send_message(message.chat.id, 'Нажмите на интересующую вас валюту:', reply_markup = keyboard)
    
@bot.callback_query_handler(func = lambda call: call.data == 'USD')
def newbutton(query):
    bot.send_message(query.message.chat.id, 'Курс USD к рублю равен' + " " + str(round(float(1 / get_exchange('USD')), 2)))

@bot.callback_query_handler(func = lambda call: call.data == 'EUR')
def newbutton(query):
    bot.send_message(query.message.chat.id, 'Курс EUR к рублю равен' + " " + str(round(float(1 / get_exchange('EUR')), 2)))
    
@bot.callback_query_handler(func = lambda call: call.data == 'GBP')
def newbutton(query):
    bot.send_message(query.message.chat.id, 'Курс GBP к рублю равен' + " " + str(round(float(1 / get_exchange('GBP')), 2)))
    
@bot.message_handler(commands=['help'])
def mychat(message):
    bot.send_message(message.chat.id, 'Чтобы получить список доступных валют по отношению к рублю, введите /exchange.\n' +
'Нажмите на интересующую вас валюту. \ n' +
'Вы получите сообщение, содержащее информацию о курсе валют')
    
    
if __name__ == '__main__':
    bot.polling(none_stop=True)
