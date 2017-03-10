import urllib2
import json

apikey = "0152bf426c1189562d39dfe4d04cee99"

anfrage = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?q=Konz,de&appid=" + apikey)

data = json.load(anfrage)

if data['weather'][0]['description'] == "clear sky":
    #setze das Bild auf Sun
    wetter = ""
elif data['weather'][0]['description'] == "rain":
    #setze das Bild auf Rain
    wetter = ""
elif data['weather'][0]['description'] == "snow":
    #setze das Bild auf Schnee
    wetter = ""
elif data['weather'][0]['description'] == "few clouds":
    #setze das Bild auf partlysun
    wetter = ""
else:
    #setze das Bild auf cloud
    wetter = ""


print (data['name'])
print ("Das Wetter in Konz ist: " + data['weather'][0]['description'])
print ("Die aktuelle Temperatur betraegt: " + str(data['main']['temp']))

