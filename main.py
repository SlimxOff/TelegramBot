import telebot
import sqlite3
import random

from telebot import types

connect = sqlite3.connect('db/BanWordDB.db', check_same_thread=False)
cursor = connect.cursor()

token = '5383745895:AAH-Y6K7aAz6Dn4ugWcl6vzgqoqdMAzP0bM'
bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def Hello_Message(message):
    if message.text == '/roll':
        message = bot.send_message(message.chat.id, 'Введите нижнюю границу диапазона')
        bot.register_next_step_handler(message, Second_Number_Step)
    else:
        x = message.text
        s = x.split()
        for i in range(0, len(s)):
            if s[i] == 'терроризм' or s[i] == 'взрывчатка' or s[i] == 'взорвем' or s[i] == 'сишка' or \
                    s[i] == 'подрыв' or s[i] == 'терракт' or s[i] == 'федералы' or s[i] == 'фсбшники' \
                    or s[i] == 'слежка' or 'теракт' or 'терорист' or 'тероризм':
                user_id = message.from_user.id
                try:
                    massage = '<<Default>>'
                    cursor.execute("INSERT INTO dangerous_asseges (user_id,user_massege) VALUES(?,?);",
                                   (user_id, massage))
                    connect.commit()
                except:
                    massage = message.text
                    m = cursor.execute('SELECT user_massege FROM dangerous_asseges WHERE user_id = ?', (user_id,))
                    n = cursor.fetchone()[0]
                    s = "" + n + "" + '\n' + "<<" + massage + ">>"
                    cursor.execute('UPDATE dangerous_asseges SET user_massege=? WHERE user_id = ?;', (s, user_id))
                    connect.commit()
                    return 0


def Second_Number_Step(message):
    global NUM_first
    NUM_first = int(message.text)
    message = bot.send_message(message.chat.id, 'Введите верхнюю границу диапазона')
    bot.register_next_step_handler(message, Result_Number_Step)


def Result_Number_Step(message):
    global NUM_second
    NUM_second = int(message.text)
    Result(message)


def Result(message):
    bot.send_message(message.chat.id, 'Случайное число:  ' + str(random.randint(NUM_first, NUM_second)))


bot.polling(none_stop=True, interval=0)
