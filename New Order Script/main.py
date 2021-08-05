import requests
import configparser
import time
import datetime
from bs4 import BeautifulSoup
import os

config = configparser.ConfigParser()
config.read("settings.ini")
URL = config["DEFAULT"]["URL"]
delay = int(config["DEFAULT"]["DELAY_TIME"])
flag = True
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
count = int(config["DEFAULT"]["start_items"])

def set_value_in_property_file(file_path, section, key, value):
    config = configparser.RawConfigParser()
    config.read(file_path)
    config.set(section,key,value)
    cfgfile = open(file_path,'w')
    config.write(cfgfile, space_around_delimiters=False)
    cfgfile.close()

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def download_drive():
    print("DOWNLOADING")
    os.system("download.py")

def get_content(html):
    global flag
    global count


    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('c-wiz', {"class":"pmHCK"})

    newCount = len(cards)

    for card in cards:
        card = card.find_all('div', class_='Q5txwe')
        print(card)

    if newCount != count:
        download_drive()
        set_value_in_property_file("settings.ini", "DEFAULT", "START_ITEMS", str(newCount))
        count = newCount

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')

while flag:
    parse()
    time.sleep(delay)


