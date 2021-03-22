import telebot
from telebot import types
from db_f import add_message
from db_f import get_random_message
from db_f import get_user_message

bot = telebot.TeleBot("1781135362:AAGS0Wtl-Wk8jmph20M8Mw16OC8CnlARAt8", parse_mode=None) #API Token


@bot.message_handler(commands=['start', 'help']) #Introduction and first message handler
def send_welcome(message):
	bot.reply_to(message, "Привет, я бот - хранитель историй о различных"
						  "профессиях. Ниже ты найдешь список доступных команд. Делись своей историей или изучай истории"
						  "других людей!\n "
						  "\nСписок доступных команд: \nПрочитать историю - /getstory \nНаписать историю - "
						  "/writestory \nПосмотреть свои публикации - /getmystory")
	print(message.from_user.id)


@bot.message_handler(content_types=['text']) #Main dialog initialization
def last_msg(message):
	if message.text == '/getstory' or message.text == 'Следующая история': #Get\next story construction
			next_story_menu = types.ReplyKeyboardMarkup(row_width=1)
			next_story = types.KeyboardButton(text="Следующая история")
			next_story_menu.add(next_story)
			bot.send_message(chat_id=message.from_user.id, text=".", reply_markup=next_story_menu)
			random_text = get_random_message()
			bot.reply_to(message, random_text)
	elif message.text == '/writestory':
		markup = types.ReplyKeyboardRemove(selective=False)
		bot.send_message(message.from_user.id, 'Отлично. Постарайся написать свою '
											   'историю максимально подробно и интересно. Люди любят чи'
											   'тать подробности и детали. Также напиши примерную '
											   'зарплату или вилку на рынке труда.', reply_markup=markup)
		bot.register_next_step_handler_by_chat_id(message.chat.id, take_story)
	elif message.text == '/getmystory': #List of user stories
		user_stories = str(get_user_message(user_id = message.from_user.id))
		print(user_stories)
		bot.reply_to(message, "Вот твои публикации: \n" + user_stories[:50])
	else:
		bot.reply_to(message, '\nСписок доступных команд: \nПрочитать историю - /getstory \nНаписать историю - '
							  '/writestory \nПосмотреть свои публикации - /getmystory')


@bot.message_handler(content_types=['text']) #Last step of dialog
def take_story(message):
	bot.reply_to(message, "Отличная история! Теперь другие люди смогут подчерпнуть твой опыт и найти своё призвание! "
						  "Всего одним сообщением - ты сделал мир лучше!")
	a = message.from_user.id
	b = message.text
	add_message(user_id=a, text=b)


bot.polling() #Bot polling/initialization