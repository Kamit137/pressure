import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('6744998769:AAE0_KtJNM9ehs4hu535LyJJa31T0SdyNY8')






# действие команд
# Большие кнопки
@bot.message_handler(commands=['start'])
def chat(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    b2 = (types.InlineKeyboardButton('Новый замер давления'))
    b5 = (types.KeyboardButton('Напоминание принять лекарства'))
    b3 = (types.InlineKeyboardButton('Регистрация/обновление данных'))
    #b6 = (types.KeyboardButton('Удалить'))
    b7 = (types.KeyboardButton('Меню'))

    markup1.add(b7,b2,b5,b3)
    bot.send_message(message.chat.id, 'Добрый день, этот бот поможет вам следить за здоровьем!',reply_markup=markup1)
    menu(message)
# Если человек прислал фото
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    marcup = types.InlineKeyboardMarkup()
    b1 = (types.InlineKeyboardButton('Ссылка хрен пойми куда',url='https://youtu.be/dQw4w9WgXcQ'))
    b2 = (types.InlineKeyboardButton('Удалить', callback_data='delete'))
    marcup.row(b1, b2)
    bot.reply_to(message, 'Достойно', reply_markup=marcup)


#Ответки кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        #bot.edit_message_text("Удалено", callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'exit':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == "body":
        bot.send_message(callback.message.chat.id, "Введите ваш возраст или обычное давление, отличающееся от средних табличных значений(пример:120/80): ")
        photo = open('/home/kamit/Документы/GitHub/pressure/sublime/7a51f5eb7fe32122f38a0a4c1ad38639.jpeg','rb')
        bot.send_photo(callback.message.chat.id, photo)
       




# Ответ на определённые фразы юзера
@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == "/id":
        bot.send_message(message.chat.id, 'Ваш ID:')
        bot.reply_to(message, f"{message.from_user.id}")
    #elif message.text == "Удалить":
     #   bot.delete_message(message.chat.id, message.message_id-1)
        

        
    elif message.text == "Меню":
        menu(message)
    elif message.text == "М":
        pass



    elif message.text == "Регистрация/обновление данных":
        photo = open('/home/kamit/Документы/GitHub/pressure/sublime/7a51f5eb7fe32122f38a0a4c1ad38639.jpeg','rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, 'Введите ваше нормальное давление, основываясь на таблице или личном опыте: ')
        bot.register_next_step_handler(message, user_pr_norm)
    

    else:
        bot.send_message(message.chat.id, 'Cам ты '+(message.text) )


    


#Вызов меню
def menu(message):
    markup2 = types.InlineKeyboardMarkup(row_width=1)
    b1 = (types.InlineKeyboardButton('Закрыть меню',callback_data='exit'))
    b4 = (types.InlineKeyboardButton('Статистика',callback_data='full_data'))
    markup2.add(b4,b1)
    bot.send_message(message.chat.id, '\nВыберите функцию:', reply_markup=markup2)








#
def user_pr_norm(message):
    n_p = message.text 
    if "\\"in n_p or "/" in n_p:
        db = sqlite3.connect('power.db')
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS pressure(id text primary key,normal_pressure text )""")
        c.execute("INSERT INTO pressure(id,normal_pressure)VALUES('%s','%s')"%(message.from_user.id,n_p))
        db.commit()
        db.close()
        bot.send_message(message.chat.id, 'Данные записаны')
        #bot.send_message(message.chat.id, 'Введите ваш возраст: ')
        #bot.register_next_step_handler(message, user_)
    else:
        bot.send_message(message.chat.id, 'Запись некорректна, попробуйте ещё раз')
        bot.register_next_step_handler(message, user_pr_norm)


# Команда id
@bot.message_handler(commands=['id'])   
def chat(message):
    bot.reply_to(message, f"Ваш ID:{message.from_user.id}")

# Чтобы бот работал многоразово
bot.polling(none_stop=True)
