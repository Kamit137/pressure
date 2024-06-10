import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('6744998769:AAE0_KtJNM9ehs4hu535LyJJa31T0SdyNY8')
#fdff
#dfd
#ssss


# действие команд
# Большие кнопки
@bot.message_handler(commands=['start'])
def chat(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    b1 = (types.KeyboardButton('Ссылка хрен пойми куда'))
    b3 = (types.KeyboardButton('Получить мем'))
    markup.add(b1, b3)
    bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    # bot.register_next_step_handler(message, on_click)


# Команда id
@bot.message_handler(commands=['id'])
def chat(message):
    bot.reply_to(message, f"Ваш ID:{message.from_user.id}")


# Если человек прислал фото
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    marcup = types.InlineKeyboardMarkup()
    b1 = (types.InlineKeyboardButton('Ссылка хрен пойми куда',
                                     url='https://www.youtube.com/watch?v=RpiWnPNTeww&list=PL0lO_mIqDDFUev1gp9yEwmwcy8SicqKbt&index=4'))
    b2 = (types.InlineKeyboardButton('Удалить', callback_data='delete'))
    marcup.row(b1, b2)

    b3 = (types.InlineKeyboardButton('Изменить', callback_data='edit'))
    marcup.row(b3)
    bot.reply_to(message, 'Достойно', reply_markup=marcup)


# Настройки для кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.edit_message_text("Удалено", callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)


# Ответ на определённые фразы юзера
@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == "id":
        bot.reply_to(message, f"Ваш ID:{message.from_user.id}")

    if message.text == "Ссылка хрен пойми куда":
        bot.send_message(message.chat.id,
                         "https://www.youtube.com/watch?v=RpiWnPNTeww&list=PL0lO_mIqDDFUev1gp9yEwmwcy8SicqKbt&index=4")
    elif message.text == "Удалить":
        bot.send_message(message.chat.id, 'Удалено')
    else:
        #bot.send_message(message.chat.id, 'Сам ты')
        
        
        bot.send_message(message.chat.id, 'Cам ты '+(message.text) )



# Чтобы бот работал многоразово
bot.polling(none_stop=True)
