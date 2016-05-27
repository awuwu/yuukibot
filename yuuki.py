import logging, os, random, ConfigParser
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram, twitter

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

api = twitter.Api(consumer_key=config.get('Twitter','consumer_key'),
		  consumer_secret=config.get('Twitter','consumer_secret'),
		  access_token_key=config.get('Twitter','access_token_key'),
		  access_token_secret=config.get('Twitter','access_token_secret'))

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
	bot.sendMessage(chat_id=chat_id, text="Awu? Glad you asked! I am a YuukiBot! Version 1.1.1 Written in Python using the libraries python-twitter and telegram! I am currently operated by @yuukari on Telegram and my source code is publically available at https://github.com/awuwu/yuukibot <3 awuwuwuwuwu~! <333")

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
updater.dispatcher.addHandler(CommandHandler('fortune', magic))
updater.dispatcher.addHandler(CommandHandler('about', about))

#aliases
updater.dispatcher.addHandler(CommandHandler('shouldi', magic))
updater.dispatcher.addHandler(CommandHandler('shouldwe', magic))
updater.dispatcher.addHandler(CommandHandler('cani', magic))
updater.dispatcher.addHandler(CommandHandler('mayi', magic))







updater.start_polling()
updater.idle()
