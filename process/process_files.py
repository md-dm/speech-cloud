	
# -*- coding: latin-1 -*-  

import os
import re
import codecs
from collections import Counter, defaultdict
import pymongo
from pymongo import Connection
import datetime


#######################################################################
## MAIN
# Start the process

#mongo ds043057.mongolab.com:43057/datafest -u <dbuser> -p <dbpassword>

connection = Connection('ds043027.mongolab.com', 43027)
db = connection['datafest']
db.authenticate("datafest", "mddm")
cloud = db['cloud']

print cloud.count()


totalCounter = Counter()

for filename in os.listdir("Discursos Presidenciales"):

	file = codecs.open("Discursos Presidenciales/" + filename, "r", "iso-8859-1")
	#print file.read().lower()

	wordsCount = re.findall('\w+', file.read().lower(), re.UNICODE)
	
	print wordsCount 
	#print wordsCount
	words_cloud = {}
	words_cloud["filename"] = filename
	
	counter = Counter(wordsCount)
	print counter

	dictionary = ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "en", "entre", "hacia", "hasta",
				  "para", "por", "sin", "sobre", "tras", "durante", "mediante", 
				  "el", "la", "los", "las", "lo", "al", "del", "un", "unas", "unos", "unas", "le", 
				  "que", "cuando", "donde", "porque", "a", "e", "i", "o", "u", "quien", "como", "quienes", "cuales", 
				  "ellos", "ellas", "cual", "si", "no", "se", 
				  "sé", "van", "también", "tambien", "ahi", "ahí", "allí", "alli",
				  "sin" ]

	#dictionary = ["a", "e", "i", "o", "u", "y", "el", "en", "la", "de", "que", "con", "un", "las", "los", "ese", "es", "eso", "esa", "esos", "la", "los", "del", "ha", "esto", "para", "por", "muy", "lo", "hay", "son", "nos", "sido", "sus", "pero", "ah"]

	for word in dictionary:
		del counter[word]


	words = []
	
	totalCounter += counter

	for k, v in counter.iteritems():
		#print k
		words.append({"text":k, "size":v})

	words_cloud["words"] = words 


	words_cloud["date"] = datetime.datetime.strptime(filename[0:8], "%Y%m%d")
	words_cloud["sdate"] = filename[0:8]

	print words_cloud
	cloud.insert(words_cloud)



#Total Words!
filename = "20121230 Palabras totales.TXT"
words_cloud = {}
words_cloud["filename"] = filename

for k, v in totalCounter.iteritems():
	#print k
	words.append({"text":k, "size":v})

	words_cloud["words"] = words 


	words_cloud["date"] = datetime.datetime.strptime(filename[0:8], "%Y%m%d")
	words_cloud["sdate"] = filename[0:8]


print words_cloud
cloud.insert(words_cloud)
