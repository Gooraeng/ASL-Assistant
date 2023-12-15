# 시간 출력 함수
# Last Update : 231216

import urllib.request as UR
from bs4 import BeautifulSoup as BS
from discord.ext import tasks
import requests

target = 'https://asphaltlegends.com/news'

original = UR.urlopen(target) ; res = requests.get(target) 

source = original.read()
source = BS(source, 'lxml')


@tasks.loop(minutes= 5)
async def get_patchnote_link():
    if res.status_code == 200:
        link = source.find_all('link')[12]['href']
        
        return link[:-3]



@tasks.loop(minutes= 5)
async def get_patchnote_title():
    if res.status_code == 200:
        soup = BS(res.text, 'html.parser')
        title = soup.select('body > main > div > div._4SheDy > section > div.relative.mx-cx.min-h-\[50vh\].bg-white.px-5.py-9.md\:px-20.md\:py-20.xl\:mx-auto.xl\:max-w-\[1110px\] > h1')[0].text
        
        return title