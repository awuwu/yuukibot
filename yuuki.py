import logging, os, random, ConfigParser, datetime 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ParseMode, InputTextMessageContent 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, InlineQueryHandler 
from pymongo import MongoClient 
from uuid import uuid4 
import telegram, twitter, re

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

client = MongoClient()

db = client['yuukibot2']

users = db.users
pts = db.points
bpts = db.bts4
gusers = db.gusers4

channels = db.channels

yuuki_version = "v1.6.0"

api = twitter.Api(consumer_key=config.get('Twitter','consumer_key'),
		  consumer_secret=config.get('Twitter','consumer_secret'),
		  access_token_key=config.get('Twitter','access_token_key'),
		  access_token_secret=config.get('Twitter','access_token_secret'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)



MENU, AWAIT_CONFIRMATION, AWAIT_INPUT, DEBUG = range(4)

YES, NO = ("Yes", "No")

state = dict()
context = dict()
values = dict()

def devChannels(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	f = channels.find({})
	lst = "Channels in system:\n"
	for y in f:
		print y
		try:
			if bot.getChat(str(y['channel'])).type != 'private':
				lst = lst + bot.getChat(str(y['channel'])).title + ": "+y['version']+"\n"
		except:
			lst = lst + str(y['channel']) + ": No version.\n"
	bot.sendMessage(chat_id,text=lst)

def escape_markdown(text):
	escape_chars = '\*_`\['
	return re.sub(r'([%s])' % escape_chars, r'\\\1', text)

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

def migrateToBPTS(username,user_id):
	n = gusers.insert_one({"username":username,"date_inserted":datetime.datetime.now(),"id":user_id,"infamy":0})
	# now fetch points from this user handle
	for x in pts.find({"username":username}):
		bpts.insert_one({"id":user_id,"point_value":x['point_value'],"date_inserted":x['date_inserted'],"giver":"Probably Yuukari","infamy": False})
	return True

def infamyCheck(id):
	n = gusers.find_one({"id":id})
	if n == None:
		return ""
	else:
		try:
			return "Infamy: "+str(n['infamy'])
		except:
			gusers.update_one({"id":id},{"$set":{"infamy":0}})
			return ""

def doInfamy(bot, update):
	winner_usr = update.message.from_user.username.lower()
	winner_usr_id = update.message.from_user.id

	call = users.find_one({"username":winner_usr})
	call2 = gusers.find_one({"id":winner_usr_id})
	if call2 == None and call != None:
		# user has not been migrated
		migrate = migrateToBPTS(winner_usr,winner_usr_id)
	if call2 == None and call == None:
		call2 = gusers.insert_one({"username":username,"date_inserted":datetime.datetime.now(),"id":winner_usr_id,"infamy":0})


	call3 = [x for x in bpts.find({"id":winner_usr_id})]
	total = 0
	if call3 != None:
		for y in call3:
			if y['infamy'] == False:
				total = total + y['point_value']
	infamy = 0
	while total >= 10000:
		total = total - 10000
		infamy = infamy + 1
	bpts.update_many({"id":winner_usr_id},{"$set": {"infamy": True}})
	gusers.update_one({"id":winner_usr_id},{"$inc": {"infamy": infamy}})
	update.message.reply_text("Points Reset! Infamy Gained: "+str(infamy)+" (You horrible monster)")

	
def points(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	points = random.choice(os.listdir(config.get('General','path')+"points/"))
        usr = str(update.message.from_user.username).lower()
	usr_id = update.message.from_user.id
	winner_usr = update.message.reply_to_message.from_user.username.lower()
	winner_usr_id = update.message.reply_to_message.from_user.id
	t = ""
        if usr_id == config.get('Telegram', 'telegram_id') or any(str(usr_id) in str(s.user.id) for s in bot.getChatAdministrators(chat_id=update.message.chat_id)):
		#winner = message.split(" @")[1].lower()
		call = users.find_one({"username":winner_usr})


		#live migration to bpts/gusers

		migrate = False

		call2 = gusers.find_one({"id":winner_usr_id})
		if call2 == None and call != None:
			# user has not been migrated
			if update.message.reply_to_message.from_user.username != None:
				migrate = migrateToBPTS(winner_usr,winner_usr_id)
		if call2 == None and call == None:
			call2 = gusers.insert_one({"username":winner_usr,"date_inserted":datetime.datetime.now(),"id":winner_usr_id,"infamy":0})

		#if call == None:
		#	users.insert_one({"username":winner,"date_inserted":datetime.datetime.now()})

		point = random.choice([150,200,250,300,350,350,400,450])
		d = {"id":winner_usr_id,"point_value":point,"date_inserted":datetime.datetime.now(),"room":str(update.message.chat_id),"giver":str(usr_id),"infamy": False}
		bpts.insert_one(d)
		# next, find how many points they currently have.
		call3 = [x for x in bpts.find({"id":winner_usr_id})]
		total = 0
		if call3 != None:
			for y in call3:
				if y['infamy'] == False:
					total = total + y['point_value']
		t = " "+str(point)+" Points to @"+update.message.reply_to_message.from_user.username+" "+infamyCheck(winner_usr_id)+"! Total: "+str(total)+" official points!"
		if migrate:
			t = t + "\n(You have also been migrated to the new points system!)"
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
	points = random.choice(os.listdir(config.get('General','path')+"points/"))
        usr = str(update.message.from_user.username).lower()
	usr_id = update.message.from_user.id
	winner_usr = update.message.reply_to_message.from_user.username.lower()
	winner_usr_id = update.message.reply_to_message.from_user.id
	t = ""
        if usr_id == config.get('Telegram', 'telegram_id') or any(str(usr_id) in str(s.user.id) for s in bot.getChatAdministrators(chat_id=update.message.chat_id)):
		#winner = message.split(" @")[1].lower()
		call = users.find_one({"username":winner_usr})


		#live migration to bpts/gusers

		migrate = False

		call2 = gusers.find_one({"id":winner_usr_id})
		if call2 == None and call != None:
			# user has not been migrated
			if update.message.reply_to_message.from_user.username != None:
				migrate = migrateToBPTS(winner_usr,winner_usr_id)
		if call2 == None and call == None:
			call2 = gusers.insert_one({"username":username,"date_inserted":datetime.datetime.now(),"id":winner_usr_id,"infamy":0})

		#if call == None:
		#	users.insert_one({"username":winner,"date_inserted":datetime.datetime.now()})

		point = 500
		d = {"id":winner_usr_id,"point_value":point,"date_inserted":datetime.datetime.now(),"room":str(update.message.chat_id),"giver":str(usr_id),"infamy": False}
		bpts.insert_one(d)
		# next, find how many points they currently have.
		call3 = [x for x in bpts.find({"id":winner_usr_id})]
		total = 0
		if call3 != None:
			for y in call3:
				if y['infamy'] == False:
					total = total + y['point_value']
		t = "THAT WAS AWESOME! 500 points to @"+update.message.reply_to_message.from_user.username+" "+infamyCheck(winner_usr_id)+"! Total: "+str(total)+" official points!"
		if migrate:
			t = t + "\n(You have also been migrated to the new points system!)"
	bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
	bot.sendDocument(chat_id=chat_id,document=open(config.get('General','path')+"win/"+points, 'rb'),caption=t)
	doUpdateMessage(bot, update)

def me(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
#	bot.sendMessage(chat_id=chat_id, text="*"+update.message.from_user.first_name+" "+message.lstrip('/me')+"*",parse_mode="Markdown")
	bot.sendMessage(chat_id=chat_id, text="What do yuu think this is, IRC? owo")

def shrug(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
#	bot.sendMessage(chat_id=chat_id, text="*"+update.message.from_user.first_name+" "+message.lstrip('/me')+"*",parse_mode="Markdown")
	bot.sendMessage(chat_id=chat_id, text="\u00AF\\_(\u30C4)_/\u00AF".decode('unicode-escape'))

def riot(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
#	bot.sendMessage(chat_id=chat_id, text="*"+update.message.from_user.first_name+" "+message.lstrip('/me')+"*",parse_mode="Markdown")
	bot.sendMessage(chat_id=chat_id, text="\xE3\x83\xBD\xE0\xBC\xBC\xE0\xBA\x88\xD9\x84\xCD\x9C\xE0\xBA\x88\xE0\xBC\xBD\xEF\xBE\x89\x20\x52\x49\x4F\x54\x20\xE3\x83\xBD\xE0\xBC\xBC\xE0\xBA\x88\xD9\x84\xCD\x9C\xE0\xBA\x88\xE0\xBC\xBD\xEF\xBE\x89".decode('utf-8'))

def twitter(bot, update):
	chat_id = update.message.chat_id
	message = update.message.text.encode('utf-8')
	usr = update.message.from_user.username
	usr_id = update.message.from_user.id
	if usr_id == config.get('Telegram', 'telegram_id'):
		st = api.PostUpdate(message.replace("/tweet",""))
		bot.sendMessage(chat_id=chat_id, text="Sent Tweet! https://www.twitter.com/"+config.get('Twitter','twitter_account')+"/status/"+str(st.id))

def magic(bot,update):
	chat_id = update.message.chat_id
	lines = open(config.get('General', 'path')+'fortune.txt').read().splitlines()
	myline =random.choice(lines)
	bot.sendMessage(chat_id=chat_id, text=myline)
	doUpdateMessage(bot, update)

def whatNumberIsThis(bot,update):
	chat_id = update.message.chat_id
	bot.sendMessage(chat_id=chat_id, text=str(update.message.reply_to_message.message_id))

def whereAmI(bot,update):
	chat_id = update.message.chat_id
	bot.sendMessage(chat_id=chat_id, text=str(chat_id))

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

def messageCount(bot, update):
	faces = ["<w<", ">w>", "owo", "uwu"]

	rang2 = random.randrange(0,len(faces)-1)
	bot.sendMessage(chat_id=update.message.chat_id,text="It's Message #"+str(update.message.message_id)+" "+faces[rang2])

def top5(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	di = gusers.find({})
	us = {}
	for x in di:
		us[x['id']] = [0,x['username'],x['infamy']]
	dn = bpts.find({})
	for y in dn:
		try:
			if y['infamy'] == False:
				us[y['id']][0] = us[y['id']][0] + y['point_value']
		except:
			print "Error"
			pass
	ls = [['undef',0,'The Collective Unconsious',0]]
	for key,value in us.iteritems():
		ls.append([key,value[0],value[1],value[2]])
	ls.sort(key=lambda tup: tup[1], reverse=True)
	tx = "Top 10 in Official Points:\n"
	i = 0
	#print ls
	try:
		while i != 11:
			tx = tx + ls[i][2].replace("@"," ") + ": "+str(ls[i][1])+" Infamy: "+str(ls[i][3])+"\n"
			i = i + 1
	except:
		pass
	tx = tx + "For full points listings globally, visit: http://me.yuu.im/points/"
	bot.sendMessage(chat_id = update.message.chat_id, text=tx)
	
	doUpdateMessage(bot, update)

def error(bot, update, error):
	logging.warning('Update "%s" caused error "%s"' % (update, error))

def inlinequery(bot, update):
	query = update.inline_query.query
	results = list()

	awu = "awu"
	rang = random.randrange(1,45)
	i = 0
	while i <= rang:
		awu = awu + "wu"
		i = i + 1

	faces = ["@w@", "<w<", ">w>", ">//w//<", "/)\\\\\\\\(\\", "@//@", "","","","","","","","","","","",""]

	rang2 = random.randrange(0,len(faces)-1)


	results.append(InlineQueryResultArticle(id=uuid4(),
						title="Awu at some folk, fam",
						input_message_content=InputTextMessageContent(awu+" "+faces[rang2]),
						)
			)
	results.append(InlineQueryResultArticle(id=uuid4(),
						title="Shrug at some folk, fam",
						input_message_content=InputTextMessageContent("\u00AF\\_(\u30C4)_/\u00AF".decode('unicode-escape')),
						)
			)
	results.append(InlineQueryResultArticle(id=uuid4(),
						title="Bot at some folk, fam",
						input_message_content=InputTextMessageContent("``` %s ```" % query, parse_mode=ParseMode.MARKDOWN),
						)
			)
	update.inline_query.answer(results)

def textHandle(bot, update):
	print str(update.message.chat.title)+": "+str(update.message.from_user.username)+": "+str(update.message.text)

updater = Updater(config.get('Telegram','api_key'))

updater.dispatcher.add_handler(CommandHandler('awuwu', awuwu))
updater.dispatcher.add_handler(CommandHandler('uwah', uwah))
updater.dispatcher.add_handler(CommandHandler('bray', bray))
updater.dispatcher.add_handler(CommandHandler('quote', quote))
updater.dispatcher.add_handler(CommandHandler('points', points))
updater.dispatcher.add_handler(CommandHandler('spiral', spiral))
updater.dispatcher.add_handler(CommandHandler('win', win))
updater.dispatcher.add_handler(CommandHandler('me', me))
updater.dispatcher.add_handler(CommandHandler('tweet', twitter))
updater.dispatcher.add_handler(CommandHandler('fortune', awu))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('moo', moo))
updater.dispatcher.add_handler(CommandHandler('top5', top5))
updater.dispatcher.add_handler(CommandHandler('top', top5))
updater.dispatcher.add_handler(CommandHandler('riot', riot))
updater.dispatcher.add_handler(CommandHandler('shrug', shrug))
updater.dispatcher.add_handler(CommandHandler('devwu', devChannels))
updater.dispatcher.add_handler(CommandHandler('reset', doInfamy))
updater.dispatcher.add_handler(InlineQueryHandler(inlinequery))

#aliases
updater.dispatcher.add_handler(CommandHandler('shouldi', magic))
updater.dispatcher.add_handler(CommandHandler('shouldwe', magic))
updater.dispatcher.add_handler(CommandHandler('cani', magic))
updater.dispatcher.add_handler(CommandHandler('mayi', magic))
updater.dispatcher.add_handler(CommandHandler('wherearewe', whereAmI))
updater.dispatcher.add_handler(CommandHandler('whatnumberisthis', whatNumberIsThis))
updater.dispatcher.add_handler(CommandHandler('whatisthis', messageCount))

#callback
# The command
#updater.dispatcher.add_handler(CommandHandler('set', set_value))
#updater.dispatcher.add_handler(CommandHandler('awu', awu))
# The answer
#updater.dispatcher.add_handler(MessageHandler([Filters.text], entered_value))
# The confirmation
#updater.dispatcher.add_handler(CallbackQueryHandler(confirm_value))
updater.dispatcher.add_handler(CallbackQueryHandler(editAwu2))
updater.dispatcher.add_error_handler(error)

#updater.dispatcher.add_handler(MessageHandler(Filters.all, textHandle))

updater.start_polling()
updater.idle()
