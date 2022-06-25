import gspread
import telebot
from aiogram import types
import pandas as pd

gc = gspread.service_account(filename="service_account.json")
sh = gc.open_by_key("19FVNJQyvx_RXcGEZ0KnZw3AvBpoirn8ipkJBAky2ZE8")
bot_token = "5503326001:AAG5UngmlbZt5o5WniLsLeHZLYF_cDPZQVk"
bot = telebot.TeleBot(bot_token)

cuisine = ""
title = ""
address = ""
phone = ""
opening_hours = ""
recommendation = ""
googlesheet_id = "19FVNJQyvx_RXcGEZ0KnZw3AvBpoirn8ipkJBAky2ZE8"

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton("Отправить информацию в таблицу")
    item_2 = types.KeyboardButton("Получить информацию из таблицы")
    markup.add(item_1)
    markup.add(item_2)
    bot.send_message(m.chat.id, "Нажмите кнопку", reply_markup=[markup])
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip()=="Отправить информацию в таблицу":
          bot.register_next_step_handler(message, add_cuisine)
    elif message.text.strip()=="Получить информацию из таблицы":
          bot.register_next_step_handler(message, get_info)

@bot.message_handler(func=lambda m: True)
def add_cuisine(message):
    global cuisine
    cuisine = message.text
    bot.send_message(message.from_user.id, "Как называется кафе?")
    bot.register_next_step_handler(message, add_title)

@bot.message_handler()
def add_title(message):
    global title
    title = message.text
    bot.send_message(message.from_user.id, "Где находится заведение?")
    bot.register_next_step_handler(message, add_address)

@bot.message_handler()
def add_address(message):
    global address
    address = message.text
    bot.send_message(message.from_user.id, "Какой телефон у заведения?")
    bot.register_next_step_handler(message, add_phone)
@bot.message_handler()
def add_phone(message):
    global phone
    phone = message.text
    bot.send_message(message.from_user.id, "Какое время работы заведения?")
    bot.register_next_step_handler(message, add_opening_hours)
@bot.message_handler()
def add_opening_hours(message):
    global opening_hours
    opening_hours = message.text
    bot.send_message(message.from_user.id, " Какое блюдо посоветуете?")
    bot.register_next_step_handler(message, add_recommendation)

@bot.message_handler()
def add_recommendation(message):
    global recommendation
    recommendation = message.text
    bot.send_message(message.from_user.id, "Большое спасибо за помощь. Ваши данные записаны")
    bot.register_next_step_handler(message, send_to_sheet)

def send_to_sheet(message):
    list = gc.open_by_key(googlesheet_id)
    list.sheet1.append_row([cuisine, title, address, phone, opening_hours, recommendation])

def get_info(message):
    goal = message.text
    worksheet = sh.get_worksheet(0)
    data_frame = pd.DataFrame(worksheet.get_all_records())
    answer = data_frame[data_frame["cuisine"]==goal].to_string(index=False, header=False)
    bot.send_message(message.chat.id, answer)
bot.polling(none_stop=True)

