import logging, os, random, ConfigParser
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from telegram import Emoji, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram, twitter

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

api = twitter.Api(consumer_key=config.get('Twitter','consumer_key'),
		  consumer_secret=config.get('Twitter','consumer_secret'),
		  access_token_key=config.get('Twitter','access_token_key'),
		  access_token_secret=config.get('Twitter','access_token_secret'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

MENU, AWAIT_CONFIRMATION, AWAIT_INPUT, DEBUG = range(4)

try:
	YES, NO = (Emoji.THUMBS_UP_SIGN.decode('utf-8'), Emoji.THUMBS_DOWN_SIGN.decode('utf-8'))
except AttributeError:
	YES, NO = (Emoji.THUMBS_UP_SIGN, Emoji.THUMBS_DOWN_SIGN)

state = dict()
context = dict()
values = dict()

def set_value(bot, update):
	chat_id = update.message.chat_id
	user_id = update.message.from_user.id
	user_state = state.get(chat_id, MENU)

	if user_state == MENU:
		state[user_id] = DEBUG
		bot.sendMessage(chat_id, text="Please enter your settings value",reply_markup=ForceReply())

def entered_value(bot, update):
	chat_id = update.message.chat_id
	user_id = update.message.from_user.id
	chat_state = state.get(user_id, MENU)

	if chat_state == DEBUG:
		del state[user_id]
		bot.sendMessage(chat_id, text="How did you get here?")

	if chat_state == AWAIT_INPUT:
		state[user_id] = AWAIT_CONFIRMATION

		context[user_id] = update.message.text
		reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(YES, callback_data=YES),
						      InlineKeyboardButton(NO, callback_data=NO)]])
		bot.sendMessage(chat_id, text="Are you sure?", reply_markup=reply_markup)

def confirm_value(bot, update):
	query = update.callback_query
	chat_id = query.message.chat_id
	user_id = query.from_user.id
	text = query.data
	user_state = state.get(user_id, MENU)
	user_context = context.get(user_id, None)

	if user_state == AWAIT_CONFIRMATION:
		del state[user_id]
		del context[user_id]
		bot.answerCallbackQuery(query.id, text="Ok!")
		if text == YES:
			values[user_id] = user_context
			bot.editMessageText(text="Changed value to %s." % values[user_id],
				chat_id=chat_id,
				message_id=query.message.message_id)
		else:
			bot.editMessageText(text="Alright, value is still %s." %
				values.get(user_id, 'not set'),
				chat_id=chat_id,
				message_id=query.message.message_id)


def awuwu(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
        bot.sendChatAction(chat_id=chat_id,
			    action=telegram.ChatAction.TYPING)
	awu = "awu"
	rang = random.randrange(1,45)
	i = 0
	while i <= rang:
		awu = awu + "wu"
		i = i + 1
	bot.sendMessage(chat_id=chat_id, text=awu)

def awu(bot, update):
	chat_id = update.message.chat_id
	user_id = update.message.from_user.id
	chat_state = state.get(user_id, MENU)

	state[user_id] = AWAIT_CONFIRMATION

	context[user_id] = update.message.text
	reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(update.message.from_user.name+": Re-roll Fortune", callback_data=YES)]])
        bot.sendChatAction(chat_id=chat_id,
			    action=telegram.ChatAction.TYPING)
	lines = open(config.get('General', 'path')+'fortune.txt').read().splitlines()
	myline =random.choice(lines)
	bot.sendMessage(chat_id=chat_id, text=myline, reply_markup=reply_markup)
	
def editAwu2(bot, update):
	query = update.callback_query
	chat_id = query.message.chat_id
	user_id = query.from_user.id
	text = query.data
	user_state = state.get(user_id, MENU)
	user_context = context.get(user_id, None)

	if user_state == AWAIT_CONFIRMATION:
		del state[user_id]
		del context[user_id]
		bot.answerCallbackQuery(query.id, text="Ok!")
		if text == YES:
			lines = open(config.get('General', 'path')+'fortune.txt').read().splitlines()
			myline =random.choice(lines)
			bot.editMessageText(chat_id=chat_id, text=myline, message_id=query.message.message_id)


def uwah(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(chat_id=chat_id, text="Uwahh! /)\\\\\\\\(\\")

def bray(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(chat_id=chat_id, text="Hee haaawwww~ @w@")

def quote(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
	lines = open(config.get('General','path')+'quotes.txt').read().splitlines()
	myline =random.choice(lines)
	if (myline.find("STICKER:") != -1):
		bot.sendSticker(chat_id=chat_id, sticker=myline.lstrip("STICKER:"))
	elif (myline.find("PHOTO:") != -1):
		bot.sendPhoto(chat_id=chat_id, photo=myline.lstrip("PHOTO:"))
	else:
		bot.sendMessage(chat_id=chat_id, text=myline)

	
def points(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"points/"))
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"points/"+points, 'rb'),caption="Points!")


def spiral(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"spiral/"))
	bot.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"spiral/"+points, 'rb'),caption="Spiral~")

def win(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"win/"))
	bot.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"win/"+points, 'rb'),caption="YOU WIN")

def me(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	bot.sendMessage(chat_id=chat_id, text="*"+update.message.from_user.first_name+" "+message.lstrip('/me')+"*",parse_mode="Markdown")

def twitter(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	usr = update.message.from_user.username
	if usr.lower() == config.get('Telegram', 'telegram_handle'):
		st = api.PostUpdate(message.replace("/tweet",""))
		bot.sendMessage(chat_id=chat_id, text="Sent Tweet! https://www.twitter.com/"+config.get('Twitter','twitter_account')+"/status/"+str(st.id))

def magic(bot,update):
	chat_id = update.message.chat_id
	lines = open(config.get('General', 'path')+'fortune.txt').read().splitlines()
	myline =random.choice(lines)
	bot.sendMessage(chat_id=chat_id, text=myline)

def about(bot,update):
	chat_id = update.message.chat_id
	bot.sendMessage(chat_id=chat_id, text="Awu? Glad you asked! I am a YuukiBot! Version 1.1.2 Written in Python using the libraries python-twitter and telegram! I am currently operated by @yuukari on Telegram and my source code is publically available at https://github.com/awuwu/yuukibot <3 awuwuwuwuwu~! <333")

def moo(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
        bot.sendChatAction(chat_id=chat_id,
			    action=telegram.ChatAction.TYPING)
	awu = "moo"
	rang = random.randrange(1,60)
	i = 0
	while i <= rang:
		awu = awu + "ooo"
		i = i + 1
	awu = awu+"~ @w@"
	bot.sendMessage(chat_id=chat_id, text=awu)


def error(bot, update, error):
	logging.warning('Update "%s" caused error "%s"' % (update, error))

updater = Updater(config.get('Telegram','api_key'))

updater.dispatcher.addHandler(CommandHandler('awuwu', awuwu))
updater.dispatcher.addHandler(CommandHandler('uwah', uwah))
updater.dispatcher.addHandler(CommandHandler('bray', bray))
updater.dispatcher.addHandler(CommandHandler('quote', quote))
updater.dispatcher.addHandler(CommandHandler('points', points))
updater.dispatcher.addHandler(CommandHandler('spiral', spiral))
updater.dispatcher.addHandler(CommandHandler('win', win))
updater.dispatcher.addHandler(CommandHandler('me', me))
updater.dispatcher.addHandler(CommandHandler('tweet', twitter))
updater.dispatcher.addHandler(CommandHandler('fortune', awu))
updater.dispatcher.addHandler(CommandHandler('about', about))
updater.dispatcher.addHandler(CommandHandler('moo', moo))

#aliases
updater.dispatcher.addHandler(CommandHandler('shouldi', magic))
updater.dispatcher.addHandler(CommandHandler('shouldwe', magic))
updater.dispatcher.addHandler(CommandHandler('cani', magic))
updater.dispatcher.addHandler(CommandHandler('mayi', magic))

#callback
# The command
updater.dispatcher.add_handler(CommandHandler('set', set_value))
#updater.dispatcher.add_handler(CommandHandler('awu', awu))
# The answer
updater.dispatcher.add_handler(MessageHandler([Filters.text], entered_value))
# The confirmation
#updater.dispatcher.add_handler(CallbackQueryHandler(confirm_value))
updater.dispatcher.add_handler(CallbackQueryHandler(editAwu2))
updater.dispatcher.add_error_handler(error)


updater.start_polling()
updater.idle()
