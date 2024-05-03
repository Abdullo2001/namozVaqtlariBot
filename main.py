from datetime import datetime
from telebot import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import sqlite3
import requests
import json
import requests

abmarkaz="6247457720:AAHQGzpg3DospmU56lFGkFOtCrTp63B6gaU"
bot=TeleBot(abmarkaz)

rm=ReplyKeyboardRemove()

touches = ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
touch1 = KeyboardButton("Toshkent")
touch2 = KeyboardButton("Andijon")
touch3 = KeyboardButton("Qo'qon")
touch4 = KeyboardButton("Namangan")
touch5 = KeyboardButton("Jizzax")
touch6 = KeyboardButton("Guliston")
touch7 = KeyboardButton("Samarqand")
touch8 = KeyboardButton("Nukus")
touch9 = KeyboardButton("Qarshi")
touch10 = KeyboardButton("Navoiy")
touch11 = KeyboardButton("Buxoro")
touch12 = KeyboardButton("Xiva")

touches.add(touch1)
touches.add(touch2)
touches.add(touch3)
touches.add(touch4)
touches.add(touch5)
touches.add(touch6)
touches.add(touch7)
touches.add(touch8)
touches.add(touch9)
touches.add(touch10)
touches.add(touch11)
touches.add(touch12)

buyruqlar1=ReplyKeyboardMarkup(resize_keyboard=True)
buyruq1=KeyboardButton("Xabarsiz ko'rish")
buyruq2=KeyboardButton("Bugungi namoz vaqtlari")
buyruq3=KeyboardButton("Haftalik namoz vaqtlari")
buyruq4=KeyboardButton("Manzilni o'zgartirish")
buyruqlar1.add(buyruq1)
buyruqlar1.add(buyruq2)
buyruqlar1.add(buyruq3)
buyruqlar1.add(buyruq4)

buyruqlar2=ReplyKeyboardMarkup(resize_keyboard=True)
buyruq5=KeyboardButton("Xabar yuborilsin")
buyruqlar2.add(buyruq5)
buyruqlar2.add(buyruq2)
buyruqlar2.add(buyruq3)
buyruqlar2.add(buyruq4)

def saralash(msg):
    xabar=str(msg.text)
    ruyhat=["Toshkent","Andijon","Qo'qon","Namangan","Jizzax","Guliston","Samarqand","Nukus","Qarshi","Navoiy","Buxoro","Xiva"]
    if xabar in ruyhat:
        conn=sqlite3.connect("data.db")

        conn.execute(f"""INSERT INTO foydalanuvchilar (chat_id,adres,xabar) VALUES ({msg.chat.id},'{xabar}','True')""")

        conn.commit()
        bot.send_message(msg.chat.id,"Manzil saqlandi. \nNamoz vaqtlari sizga doimiy yuborib turiladi.\nXabar olishni hohlamasangiz. \nXabarsiz ko'rishni tanlang",reply_markup=buyruqlar1)
    else:
        bot.send_message(msg.chat.id,"Manzil noto'g'ri kiritildi. \nPastdagi tugmalar yordamida manzilingizni yuboring")
        bot.register_next_step_handler(msg,saralash)

def change_adres(msg):
    conn=sqlite3.connect("data.db")
    conn.execute(f"""UPDATE foydalanuvchilar set adres ='{str(msg.text)}' WHERE chat_id={msg.chat.id}""")
    baza=conn.execute(f"""SELECT xabar FROM foydalanuvchilar WHERE chat_id='{msg.chat.id}'""")
    for i in baza:
        if i[0]=="True":
            bot.send_message(msg.chat.id,"Manzil o'zgartirildi",reply_markup=buyruqlar1)
        elif i[0]=="False":
            bot.send_message(msg.chat.id,"Manzil o'zgartirildi",reply_markup=buyruqlar2)
    conn.commit()

def yubor(moment,vil,time):
    conn=sqlite3.connect("data.db")
    baza=conn.execute(f"""SELECT chat_id FROM foydalanuvchilar""")
    conn.commit()
    for i in baza:
        bot.send_message(int(i[0]),f"{moment} vaqti bo'ldi. \n({vil} shahri bo'yicha)\n\n{time}")


@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,f"Salom {msg.from_user.username}")
    tek=0
    conn=sqlite3.connect("data.db")
    baza=conn.execute(f"""SELECT chat_id,adres,xabar FROM foydalanuvchilar WHERE chat_id={msg.chat.id}""")
    conn.commit()
    for i in baza:
        tek=[i[1],i[2]]
    if tek==0:
        bot.send_message(msg.chat.id,f"Yashash manzilingizni tanlang",reply_markup=touches)
        bot.register_next_step_handler(msg,saralash)
    elif tek[1]=='True':
        bot.send_message(msg.chat.id,f"Siz avval ro'yhatdan o'tgansiz.\nSizning manzilingiz {tek[0]}\nAgar o'zgartirmoqchi bo'lsangiz 'Manzilni o'zgartirish' tugmasini bosing",reply_markup=buyruqlar1)
    elif tek[1]=='False':
        bot.send_message(msg.chat.id,f"Siz avval ro'yhatdan o'tgansiz.\nSizning manzilingiz {tek[0]}\nAgar o'zgartirmoqchi bo'lsangiz 'Manzilni o'zgartirish' tugmasini bosing",reply_markup=buyruqlar2)
    
    


@bot.message_handler(content_types=['text'])
def matn(msg):
    xabar=str(msg.text)
    if xabar=="Xabarsiz ko'rish":
        conn=sqlite3.connect("data.db")
        conn.execute(f"""UPDATE foydalanuvchilar set xabar ='False' WHERE chat_id={msg.chat.id}""")
        conn.commit()
        bot.send_message(msg.chat.id,"Endi sizga xabar yuborilmaydi",reply_markup=buyruqlar2)
    elif xabar=="Xabar yuborilsin":
        conn=sqlite3.connect("data.db")
        conn.execute(f"""UPDATE foydalanuvchilar set xabar ='True' WHERE chat_id={msg.chat.id}""")
        conn.commit()
        bot.send_message(msg.chat.id,"Endi sizga xabar yuboriladi",reply_markup=buyruqlar1)
    elif xabar=="Bugungi namoz vaqtlari":
        conn=sqlite3.connect("data.db")
        baza=conn.execute(f"""SELECT chat_id,adres FROM foydalanuvchilar WHERE chat_id={msg.chat.id}""")
        conn.commit()
        for i in baza:
            response=requests.get(f"https://islomapi.uz/api/present/day?region={i[1]}")
            res=response.json()
            bot.send_message(msg.chat.id,f"Tong saharlik: {res['times']['tong_saharlik']}\nQuyosh: {res['times']['quyosh']}\nPeshin: {res['times']['peshin']}\nAsr: {res['times']['asr']}\nShom iftor: {res['times']['shom_iftor']}\nHufton: {res['times']['hufton']}")
    elif xabar=="Haftalik namoz vaqtlari":
        conn=sqlite3.connect("data.db")
        baza=conn.execute(f"""SELECT chat_id,adres FROM foydalanuvchilar WHERE chat_id={msg.chat.id}""")
        conn.commit()
        for j in baza:
            response=requests.get(f"https://islomapi.uz/api/present/week?region={j[1]}")
            res=response.json()
            txt=""
            for i in res:
                txt+=f"{i['weekday']}\n\nTong saharlik: {i['times']['tong_saharlik']}\nQuyosh: {i['times']['quyosh']}\nPeshin: {i['times']['peshin']}\nAsr: {i['times']['asr']}\nShom iftor: {i['times']['shom_iftor']}\nHufton: {i['times']['hufton']}\n\n"
            bot.send_message(msg.chat.id,txt)
    elif xabar=="Manzilni o'zgartirish":
        bot.send_message(msg.chat.id,f"Yashash manzilingizni tanlang",reply_markup=touches)
        bot.register_next_step_handler(msg,change_adres)






current_time = datetime.now().time()

formatted_time = current_time.strftime("%H:%M")

l=["Toshkent","Andijon","Qoqon","Namangan","Jizzax","Guliston","Samarqand","Nukus","Qarshi","Navoiy","Buxoro","Xiva"]
if formatted_time=="00:00":
    for i in l:
        # f=open(f"{i}.json","w")
        response=requests.get(f"https://islomapi.uz/api/present/day?region={i}")
        res=response.json()
        # vaqt=res["times"]
        # f.write(vaqt)
        # f.close()
        conn=sqlite3.connect("data.db")
        conn.execute(f"""UPDATE vaqtlar set saharlik='{res['times']['tong_saharlik']}' WHERE viloyat={i}""")
        conn.execute(f"""UPDATE vaqtlar set saharlik='{res['times']['quyosh']}' WHERE viloyat={i}""")
        conn.execute(f"""UPDATE vaqtlar set saharlik='{res['times']['peshin']}' WHERE viloyat={i}""")
        conn.execute(f"""UPDATE vaqtlar set saharlik='{res['times']['asr']}' WHERE viloyat={i}""")
        conn.execute(f"""UPDATE vaqtlar set saharlik='{res['times']['shom_iftor']}' WHERE viloyat={i}""")
        conn.commit()

for i in l:
    conn=sqlite3.connect("data.db")
    baza=conn.execute(f"""SELECT saharlik,quyosh,peshin,asr,shom FROM vaqtlar WHERE viloyat='{i}'""")
    for j in baza:
        if formatted_time==j[0]:
            yubor("saharlik",i,j[0])
        if formatted_time==j[1]:
            yubor("quyosh",i,j[1])
        if formatted_time==j[2]:
            yubor("peshin",i,j[2])
        if formatted_time==j[3]:
            yubor("asr",i,j[3])
        if formatted_time==j[4]:
            yubor("shom",i,j[4])
    conn.commit()

bot.infinity_polling()