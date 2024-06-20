import telebot
import csv
from telebot import types
n_p = '120/80'

x = open('n.txt','a')
bot = telebot.TeleBot('6744998769:AAE0_KtJNM9ehs4hu535LyJJa31T0SdyNY8')




# действие команд
# Большие кнопки
@bot.message_handler(commands=['start'])
def chat(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    b2 = (types.InlineKeyboardButton('Новый замер давления'))
    b5 = (types.KeyboardButton('Напоминание принять лекарства'))
    b3 = (types.InlineKeyboardButton('Установить нормальное давление'))
    #b6 = (types.KeyboardButton('Удалить'))
    b7 = (types.KeyboardButton('Все замеры'))

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
        
    elif message.text.lower() == "все замеры":
    	with open('pressure.csv','r') as f:
    		r = csv.reader(f)
    		w = ''
    		for row in r:
    			w += ', '.join(row) + '\n'
    		w= w.replace(', ', '   |   ')
    		bot.send_message(message.chat.id, w)

        
    elif message.text == "Меню":
        menu(message)
    elif message.text == "Новый замер давления":
        set_data(message)



    elif message.text == "Установить нормальное давление":
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
    
    markup2.add(b1)
    bot.send_message(message.chat.id, '\nВыберите функцию:', reply_markup=markup2)








#устновка норм давления
def user_pr_norm(message):
	idu = message.from_user.id
	n_p_l = message.text 
	if "\\"in n_p_l or "/" in n_p_l:
		zap_n_p(n_p_l, idu)
		bot.send_message(message.chat.id, 'Данные записаны')
	else:
	    bot.send_message(message.chat.id, 'Запись некорректна, попробуйте ещё раз')
	    bot.register_next_step_handler(message, user_pr_norm)

def set_data(message):
	if (message.from_user.id) in norm:
		bot.send_message(message.chat.id, 'Запишите замеренное давлени: ')
		bot.register_next_step_handler(message, set_data2)
	else:
		photo = open('/home/kamit/Документы/GitHub/pressure/sublime/7a51f5eb7fe32122f38a0a4c1ad38639.jpeg','rb')
		bot.send_photo(message.chat.id, photo)
		bot.send_message(message.chat.id, 'Введите ваше нормальное давление, основываясь на таблице или личном опыте: ')
		bot.register_next_step_handler(message, user_pr_norm)
def set_data2(message):
	now_d = message.text

	if "\\"in now_d or "/" in now_d:
		with open('pressure.csv','a') as f:
			r = csv.writer(f)
			r.writerow([message.from_user.id,norm[message.from_user.id], now_d])
		bot.send_message(message.chat.id, 'Данные записаны')
		f.close()
	else:
		bot.send_message(message.chat.id, 'Запись некорректна, попробуйте ещё раз')
		bot.register_next_step_handler(message, set_data)


'''-----------------------------------------------------------------------------------------------------'''

def zap_n_p(n_p_l, idu):
	idu = str(idu)
	boo = False
	c = ''
	with open('n.txt') as x:

		for i in (x):    
			g = [q for q in i.split(', ')]
			
			if g[0] ==idu:
				c = g[0]+', '+g[1]
				boo = True

	if boo == False:
		with open ('n.txt', 'a') as f:
			f.write('\n'+idu+', '+n_p_l)
			print(0)
	else:
		with open ('n.txt', 'r') as f:
			old_data = f.read()
		print(old_data)
		new_data = old_data.replace(c, (idu+', '+n_p_l+'\n'))
		with open ('n.txt', 'w') as f:
			f.write(new_data)
'''-----------------------------------------------------------------------------------------------------'''
 
@bot.message_handler(commands=['id'])   
def chat(message):
    bot.reply_to(message, f"Ваш ID:{message.from_user.id}")

# Чтобы бот работал многоразово
bot.polling(none_stop=True)
