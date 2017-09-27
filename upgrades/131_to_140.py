import logging, os, random, ConfigParser, datetime
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from telegram import Emoji, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from pymongo import MongoClient
import telegram, twitter

client = MongoClient()

db = client['yuukibot2']

users = db.users
pts = db.points
bpts = db.bts
gusers = db.gusers

