import telebot
import sqlite3
from telebot import types
import smtplib

token = 'your bot token'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):

	user_id = [message.chat.id, 'none']

	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS users_data(
 		id INTEGER,
 		stock TEXT
 		)""")
	connect.commit()

	people_id = message.chat.id
	cursor.execute(f"SELECT id FROM users_data WHERE id = {people_id}")
	data = cursor.fetchone()

	if data is None:
		cursor.execute("INSERT INTO users_data VALUES (?, ?)", user_id)
		connect.commit()
		bot.send_message(message.chat.id,"Привет ✌️")
	else:
		bot.send_message(message.chat.id, "С возвращением!")

	#  Кнопки, которые появляются при старте
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	tesla = types.KeyboardButton("Tesla")
	markup.add(tesla)
	facebook = types.KeyboardButton("Facebook")
	markup.add(facebook)
	google = types.KeyboardButton("Google")
	markup.add(google)
	bmw = types.KeyboardButton("BMW")
	markup.add(bmw)
	bot.send_message(message.chat.id, 'Этот бот позволяет выбрать одну акцию из списка и получать по ней уведомления', reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete(message):

	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()
	people_id = message.chat.id

	cursor.execute(f"DELETE FROM users_data WHERE id = {people_id}")
	connect.commit()

	bot.send_message(message.chat.id, "Вы удалены из базы. Уведомлений больше не будет")


@bot.message_handler(commands=['config'])
def config(message):

	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()
	people_id = message.chat.id

	cursor.execute(f"SELECT stock FROM users_data WHERE id = {people_id}")
	config = cursor.fetchone()[0]

	bot.send_message(message.chat.id, f"Вы подписаны на {config}")



@bot.message_handler(content_types='text')
def message_reply(message):

	connect = sqlite3.connect('users.db')
	cursor = connect.cursor()

	stock = [message.text]

	my_email = "email to send from"
	password = "password from this email"

	if message.text == "Tesla":
		cursor.execute(f"UPDATE users_data SET stock=(?) WHERE id={message.chat.id}", stock)
		connect.commit()

		bot.send_message(message.chat.id, f"Готово!\nУведомления по {message.text} настроены")

	elif message.text == "Facebook":
		cursor.execute(f"UPDATE users_data SET stock=(?) WHERE id={message.chat.id}", stock)
		connect.commit()

		bot.send_message(message.chat.id, f"Готово!\nУведомления по {message.text} настроены")

	elif message.text == "Google":
		cursor.execute(f"UPDATE users_data SET stock=(?) WHERE id={message.chat.id}", stock)
		connect.commit()

		bot.send_message(message.chat.id, f"Готово!\nУведомления по {message.text} настроены")

	elif message.text == "BMW":
		cursor.execute(f"UPDATE users_data SET stock=(?) WHERE id={message.chat.id}", stock)
		connect.commit()

		bot.send_message(message.chat.id, f"Готово!\nУведомления по {message.text} настроены")
	else:
		with smtplib.SMTP("smtp.gmail.com", 587) as connection:
			connection.starttls()
			connection.login(user=my_email, password=password)
			connection.sendmail(
				from_addr=my_email,
				to_addrs="email to send to",
				msg=f"Subject:{message.chat.username}\n\n{message.text.encode('utf-8')}"
			)


bot.infinity_polling()