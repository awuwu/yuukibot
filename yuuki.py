import logging, os, random, ConfigParser, datetime
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from telegram import Emoji, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from pymongo import MongoClient
import telegram, twitter

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

client = MongoClient()

db = client['yuukibot2']

users = db.users
pts = db.points

channels = db.channels

yuuki_version = "v1.2.2"

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

def doChannelCheck(channel):
	call = channels.find_one({"channel":channel})
	if call == None:
		post = {
			"channel":channel,
			"version":yuuki_version
			}
		channels.insert_one(post)
		return True
	else:
		if call['version'] != yuuki_version:
			channels.update_one({"channel":channel},{"$set": {"version": str(yuuki_version)}})
			return True
		return False

def doUpdateMessage(bot, update):
	if doChannelCheck(update.message.chat_id):
		bot.sendMessage(update.message.chat_id, text="Awu! Looks like this is the first time I've been run in this chat with my new version! Check out https://github.com/awuwu/yuukibot/wiki/Commands for more info! My latest version is "+yuuki_version+"! Thanks for having me! <3")

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

	faces = ["@w@", "<w<", ">w>", ">//w//<", "/)\\\\\\\\(\\", "@//@", "","","","","","","","","","","",""]

	rang2 = random.randrange(0,len(faces)-1)

	bot.sendMessage(chat_id=chat_id, text=awu+" "+faces[rang2])

	doUpdateMessage(bot, update)

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

	doUpdateMessage(bot, update)
	
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
	doUpdateMessage(bot, update)


def bray(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)

	faces = ["@w@", "<w<", ">w>", ">//w//<", "/)\\\\\\\\(\\", "@//@", ""]

	rang2 = random.randrange(0,len(faces)-1)

	bot.sendMessage(chat_id=chat_id, text="Hee haaawwww~ "+faces[rang2])
	doUpdateMessage(bot, update)


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
	doUpdateMessage(bot, update)


	
def points(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"points/"))
        usr = update.message.from_user.username
	t = ""
	if message.find(" @") != -1:
	        if usr.lower() == config.get('Telegram', 'telegram_handle') or usr.lower() == "mochafawx":
			winner = message.split(" @")[1].lower()
			call = users.find_one({"username":winner})
			if call == None:
				users.insert_one({"username":winner,"date_inserted":datetime.datetime.now()})
			point = random.randrange(100,500)
			d = {"username":winner,"point_value":point,"date_inserted":datetime.datetime.now()}
			pts.insert_one(d)
			# next, find how many points they currently have.
			call2 = [x for x in pts.find({"username":winner})]
			total = 0
			if call2 != None:
				for y in call2:
					total = total + y['point_value']
			t = " "+str(point)+" Points to @"+message.split(" @")[1]+"! Total: "+str(total)+" official points!"
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"points/"+points, 'rb'),caption="Points!"+t)
	doUpdateMessage(bot, update)



def spiral(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"spiral/"))
	bot.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"spiral/"+points, 'rb'),caption="Spiral~")
	doUpdateMessage(bot, update)


def win(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"win/"))
        usr = update.message.from_user.username
	t = ''
        if usr.lower() == config.get('Telegram', 'telegram_handle') or usr.lower() == "mochafawx":
		winner = message.split(" @")[1].lower()
		call = users.find_one({"username":winner})
		if call == None:
			users.insert_one({"username":winner,"date_inserted":datetime.datetime.now()})
		point = 500
		d = {"username":winner,"point_value":point,"date_inserted":datetime.datetime.now()}
		pts.insert_one(d)
		# next, find how many points they currently have.
		call2 = [x for x in pts.find({"username":winner})]
		total = 0
		if call2 != None:
			for y in call2:
				total = total + y['point_value']
		t = " "+str(point)+" Points to @"+message.split(" @")[1]+" for the win! Total: "+str(total)+" official points!"
	bot.sendChatAction(chat_id=chat_id,action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"win/"+points, 'rb'),caption="THAT WAS AWESOME! "+t)
	doUpdateMessage(bot, update)


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
	doUpdateMessage(bot, update)

def about(bot,update):
	chat_id = update.message.chat_id
	bot.sendMessage(chat_id=chat_id, text="Awu? Glad you asked! I am a YuukiBot! Version "+yuuki_version+" Written in Python using the libraries python-twitter and telegram! I am currently operated by @yuukari on Telegram and my source code is publically available at https://github.com/awuwu/yuukibot <3 awuwuwuwuwu~! <333")
	doUpdateMessage(bot, update)


def moo(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
        bot.sendChatAction(chat_id=chat_id,
			    action=telegram.ChatAction.TYPING)
	awu = "moo"
	rang = random.randrange(1,20)
	i = 0
	while i <= rang:
		awu = awu + "ooo"
		i = i + 1
	awu = awu+"~ "

	faces = ["@w@", "<w<", ">w>", ">//w//<", "/)\\\\\\\\(\\", "@//@", ""]

	rang2 = random.randrange(0,len(faces)-1)
	
	awu = awu+faces[rang2]

	bot.sendMessage(chat_id=chat_id, text=awu)

	doUpdateMessage(bot, update)


def top5(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	di = users.find({})
	us = {}
	for x in di:
		us[x['username']] = 0
	dn = pts.find({})
	for y in dn:
		try:
			us[y['username']] = us[y['username']] + y['point_value']
		except:
			print "Error"
			pass
	ls = [('undef',0)]
	for key,value in us.iteritems():
		ls.append((key,value))
	ls.sort(key=lambda tup: tup[1], reverse=True)
	tx = "Top 5 in Official Points:\n"
	i = 0
	while i != 6:
		tx = tx + ls[i][0].replace("@"," ") + ": "+str(ls[i][1])+"\n"
		i = i + 1
	tx = tx + "For full points listings globally, visit: http://me.yuu.im/points/"
	bot.sendMessage(chat_id = update.message.chat_id, text=tx)
	

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
updater.dispatcher.addHandler(CommandHandler('top5', top5))
updater.dispatcher.addHandler(CommandHandler('top', top5))

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
