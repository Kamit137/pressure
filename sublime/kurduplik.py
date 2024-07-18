import telebot
import csv
from telebot import types
import time

n_p = '120/80'

x = open('n.txt','a')
bot = telebot.TeleBot('6744998769:AAE0_KtJNM9ehs4hu535LyJJa31T0SdyNY8')




# действие команд
# Большие кнопки
@bot.message_handler(commands=['start'])
def chat(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    b2 = (types.InlineKeyboardButton('Новый замер давления'))
    b5 = (types.KeyboardButton('лох'))
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

    


#Вызов меню
def menu(message):
    markup2 = types.InlineKeyboardMarkup(row_width=1)
    b1 = (types.InlineKeyboardButton('Закрыть меню',callback_data='exit'))
    
    markup2.add(b1)
    bot.send_message(message.chat.id, '\nВыберите функцию:', reply_markup=markup2)






def user_pr_norm1(message):
	photo = open('/home/kamit/Документы/GitHub/pressure/sublime/7a51f5eb7fe32122f38a0a4c1ad38639.jpeg','rb')
	bot.send_photo(message.chat.id, photo)
	bot.send_message(message.chat.id, 'Введите ваше нормальное давление, основываясь на таблице или личном опыте в формате 120/80 или 120\\80: ')
	bot.register_next_step_handler(message, user_pr_norm)

#устновка норм давления
def user_pr_norm(message):
	idu = message.from_user.id
	n_p_l = message.text 
	if proverka(n_p_l)!='Err':
		zap_n_p(n_p_l, idu)
		bot.send_message(message.chat.id, 'Данные записаны')
	else:
	    bot.send_message(message.chat.id, 'Запись некорректна, попробуйте ещё раз')
	    bot.register_next_step_handler(message, user_pr_norm)

def set_data(message):
	T = True
	idu = message.from_user.id
	for i in open('n.txt').readlines():
		if str(idu) in i:
			T = False
	if T == False:
		bot.send_message(message.chat.id, 'Запишите замеренное давлени в формате 120/80 или 120\\80: ')
		bot.register_next_step_handler(message, set_data2)
	else:
		user_pr_norm1(message)
def set_data2(message):
	now_d = message.text
	if proverka(now_d)!='Err':
		with open('pressure.csv','a') as f:
			r = csv.writer(f)
			d1 = time.strftime("%H:%M:%S, %d.%m.%Y")
			r.writerow([str(message.from_user.id), str(now_d), d1])
		with open('n.txt') as f:
			for i in f:
				
				x = [t for t in i.split(', ')]
				
				if '\\' in now_d:
					now = [t for t in now_d.split('\\')]
				elif '/' in now_d:
					now = [t for t in now_d.split('/')]
				
				
				if str(x[0]) == str(message.from_user.id):
					

					if '\\' in x[1]:
						s = (x[1]).split('\\')
					elif '/' in x[1]:
						s = (x[1]).split('/')			
					s2 = str(int(s[1]))
					s[1] = s2

					if abs(int(s[0]) - int(now[0]))<6:
						if abs(int(s[1]) - int(now[1]))<6:
							bot.send_message(message.chat.id, 'Всё в порядке!')
						else:
							bot.send_message(message.chat.id, 'Давление далеко от нормы!')
					else:
						bot.send_message(message.chat.id, 'Давление далеко от нормы!')

		
		f.close()
	else:
		bot.send_message(message.chat.id, 'Запись некорректна, попробуйте ещё раз')
		bot.register_next_step_handler(message, set_data2)
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
	else:
		with open ('n.txt', 'r') as f:
			old_data = f.read()
		new_data = old_data.replace(c, (idu+', '+n_p_l+'\n'))
		with open ('n.txt', 'w') as f:
			f.write(new_data)
'''- `----------------------------------------------------------------------------------------------------'''
 
@bot.message_handler(commands=['id'])   
def chat(message):
    bot.reply_to(message, f"Ваш ID:{message.from_user.id}")




def proverka(message):
	now = message

	if len(now) >3 and (now.count('/')==1 or now.count('\\')==1):
		if now.count('/')==1:
			e = now.split('/')
		elif now.count('\\')==1:
		
			e = now.split('\\')
		
		if 10<int(e[0])<200 and 10<int(e[1])<200:

			return message
	return 'Err'








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
    			if str(row[0])== str(message.from_user.id):
    				w += ', '.join(row) + '\n'
    		w= w.replace(', ', '   |   ')
    		
    		bot.send_message(message.chat.id,'id   |   pressure   |   date+time')
    		if len(w)>0:
    			bot.send_message(message.chat.id,w)
    		else:
    			bot.send_message(message.chat.id,'Пока записей нет')

        
    elif message.text == "Меню":
        menu(message)
    elif message.text == "Новый замер давления":
        set_data(message)



    elif message.text == "Установить нормальное давление":
        user_pr_norm1(message)
    

    else: 
        bot.send_message(message.chat.id, 'Cам ты '+(message.text) )


# Чтобы бот работал многоразово
bot.polling(none_stop=True)
	