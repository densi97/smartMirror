#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import json

apikey = "b09b49674e484230a8c3fd17f4f83458"
hostname = "https://newsapi.org/v1/articles?source="

def anfrage(source):
    url = hostname + str(source) + "&sortBy=top" + "&apiKey="  + apikey
    anfrage = urllib2.urlopen(url)
    return json.load(anfrage)

#bild
data_bild = anfrage("bild")

#ausgabe
print("Das sind die Bild Nachrichten!")
for i in range(3):
    print(str(i+1) + " " + data_bild['articles'][i]['title'])
    print(data_bild['articles'][i]['description'])
    
