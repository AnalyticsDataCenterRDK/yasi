# -*- coding: utf-8 -*-
import requests
import telebot

bot = telebot.TeleBot('6087458412:AAHlahYjK-f4T1007dDLY63vTn2xt59Fmdk')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Введите название компании:')


def search_company(company_name):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
    }

    data = {
        'query': company_name
    }

    url = 'https://egrul.nalog.ru/'
    resp = requests.post(url, data=data, headers=header)
    src = resp.json()
    t = src["t"]

    new_url = f'https://egrul.nalog.ru/search-result/{t}?r=1667326395502&_=1667326395502'
    resp2 = requests.get(new_url)
    src2 = resp2.json()
    result = ''
    for i in src2["rows"]:
        result += f'ФИО {i["n"]} ИНН {i["i"]} ОГРНИП {i["o"]}\n'
    return result


@bot.message_handler(content_types=['text'])
def send_info(message):
    company_name = message.text
    otvet = search_company(company_name)
    if len(otvet) > 4095:
        for x in range(0, len(otvet), 4095):
            bot.reply_to(message, text=otvet[x:x + 4095])
    else:
        bot.reply_to(message, text=otvet)


bot.polling()