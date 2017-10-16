# -*- coding: utf-8 -*-
# smartmirror.py
# requirements
# requests, feedparser, traceback, Pillow

from Tkinter import *
import locale
import threading
import time
import requests
import json
import traceback
import feedparser
import urllib2

from PIL import Image, ImageTk
from contextlib import contextmanager

LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 24 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
latitude = None # Set this if IP location lookup does not work for you (must be a string)
longitude = None # Set this if IP location lookup does not work for you (must be a string)
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18
apikey = "0152bf426c1189562d39dfe4d04cee99"

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter
icon_lookup = {
    'clear-day': "assets/Sun.png",  # clear sky day
    'wind': "assets/Wind.png",   #wind
    'cloudy': "assets/Cloud.png",  # cloudy day
    'partly-cloudy-day': "assets/PartlySunny.png",  # partly cloudy day
    'rain': "assets/Rain.png",  # rain day
    'snow': "assets/Snow.png",  # snow day
    'snow-thin': "assets/Snow.png",  # sleet day
    'fog': "assets/Haze.png",  # fog day
    'clear-night': "assets/Moon.png",  # clear sky night
    'partly-cloudy-night': "assets/PartlyMoon.png",  # scattered clouds night
    'thunderstorm': "assets/Storm.png",  # thunderstorm
    'tornado': "assests/Tornado.png",    # tornado
    'hail': "assests/Hail.png"  # hail
}


class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

class News(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent,bg="black")
        image = Image.open("assets/Newspaper.png")
        image = image.resize((50,50),Image.ANTIALIAS)
        image = image.convert("RGB")
        photo = ImageTk.PhotoImage(image)

        #bild
        data_bild = self.anfrage("bild")

        for i in range(5):
            text = str(i+1) +". " + data_bild['articles'][i]['title']
            self.textlbl = Label(self,text= text, font=("Helvetica", small_text_size), fg="white", bg="black")
            self.textlbl.pack(side=TOP, anchor=W, pady=10)
            
    def anfrage(self, source):
        apikey = "b09b49674e484230a8c3fd17f4f83458"
        hostname = "https://newsapi.org/v1/articles?source="
        url = hostname + str(source) + "&sortBy=top" + "&apiKey="  + apikey
        anfrage = urllib2.urlopen(url)
        return json.load(anfrage)
      
class Weather(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent,bg="black")
        anfrage = urllib2.urlopen("http://api.openweathermap.org/data/2.5/weather?q=Konz,de&appid=" + apikey)
        data = json.load(anfrage)
        if data['weather'][0]['description'] == "clear sky":
            image = Image.open("assets/Sun.png")
            wettervs = "sonnig"
        elif data['weather'][0]['description'] == "rain":
            image = Image.open("assets/Rain.png")
            wettervs = "regnerisch"
        elif data['weather'][0]['description'] == "snow":
            image = Image.open("assets/Snow.png")
            wettervs = "verschneit"
        elif data['weather'][0]['description'] == "few clouds":
            image = Image.open("assets/PartlySunny.png")
            wettervs = "bewoelkt"
        else:
            image = Image.open("assets/Cloud.png")
            wettervs = "wolkig"
        
        image = image.resize((100, 100), Image.ANTIALIAS)
        image = image.convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.iconLbl = Label(self, bg='black', image=photo)
        self.iconLbl.image = photo
        self.iconLbl.pack(side=LEFT, anchor=N)
        
        text = data['name']
        self.textlbl = Label(self, text = text,width= 100, font=("Helvetica", small_text_size), fg="white", bg="black")
        self.textlbl.pack(side=TOP, anchor=E)

        wetter = "Das Wetter ist: " + wettervs
        self.wetterlbl = Label(self, text = wetter,width= 100, font=("Helvetica", small_text_size), fg="white", bg="black")
        self.wetterlbl.pack(side=TOP, anchor=E)

        tmp = int(data['main']['temp'] - 273.15)
        temperatur ="Die aktuelle Temperatur beträgt: " + str(tmp) + "°C"
        self.templbl = Label(self, text = temperatur,width= 100, font=("Helvetica", small_text_size), fg="white", bg="black")
        self.templbl.pack(side=TOP, anchor=E)
        

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.tk.title("Mein SmartMirror")
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = True
        self.tk.attributes("-fullscreen", self.state)
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<KP_Enter>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        # clock
        self.clock = Clock(self.topFrame)
        self.clock.pack(side=RIGHT, anchor=N, padx=100, pady=60)
        # weather
        self.weather = Weather(self.topFrame)
        self.weather.pack(side=LEFT, anchor=N, padx=100, pady=100)
        # news
        self.news = News(self.bottomFrame)
        self.news.pack(side=BOTTOM, anchor=N, padx=200, pady=100)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"

if __name__ == '__main__':
    w = FullscreenWindow()
    w.tk.mainloop()

