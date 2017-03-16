#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import urllib2
import json

#hostname = "https://newsapi.org/v1/sources?"
#language = "language=de&country=de"
apikey = "b09b49674e484230a8c3fd17f4f83458"
#apiurl = "&apiKey=" + apikey
#sourcebild = "&source=bild"
#sortBy = "&sortBysAvailable=popular"
testurl = "https://newsapi.org/v1/articles?source=bild&sortBy=top&apiKey=" + apikey
test2url = "https://newsapi.org/v1/articles?source=sky-sports-news&language=de&country=de&sortBy=top&apiKey=" + apikey
anfrage = urllib2.urlopen(testurl)
anfrage2 = urllib2.urlopen(test2url)
data = json.load(anfrage)
data2 = json.load(anfrage2)
print("Das sind die Sport-Nachrichten!")
print(data2['articles'][0]['title'])
print(data2['articles'][1]['title'])
print(data2['articles'][2]['title'])
print(data2['articles'][3]['title'])
print("Das sind die Bild Nachrichten!")
print(data['articles'][0]['title'])
print(data['articles'][1]['title'])
print(data['articles'][2]['title'])
print(data['articles'][3]['title'])
