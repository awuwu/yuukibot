from pymongo import MongoClient

import math, datetime

client = MongoClient()
db = client['yuukibot2']

users = db.users
pts = db.points

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
	# key = username 
	# value = total points
	a = int(50 * math.ceil(float(value) / 50))
	b = value
	print str(key) + ": Total pts - "+str(b)+" // Round: "+str(a)+" // Total gain:" + str(a - b)
	v = a - b
	d = {"username":str(key),"point_value":v,"date_inserted":datetime.datetime.now()}
	pts.insert_one(d)
