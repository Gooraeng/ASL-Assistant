# 시간 출력 함수
# Last Update : 231216

import requests

from bs4 import BeautifulSoup as BS
from discord.ext import tasks
from discord import Embed
from .print_time import get_UTC

target = 'https://asphaltlegends.com/news/drive-syndicate-8'

res = requests.get(target)
html = res.text
soup = BS(html, 'html.parser')


p_tags = 'ck ck-content a6aJuu'

@tasks.loop(minutes= 5)
async def get_patchnote_link():
    if res.status_code == 200:
        link = soup.find_all('link')[12]['href'][:-3]
        
        return link
    
    else:
        return None


@tasks.loop(minutes= 5)
async def get_patchnote_embed():
    if res.status_code == 200:
        title = soup.find_all(class_ = 'text-h3 pb-4 uppercase')[0].text
        date = soup.find_all(class_ = 'text-lg font-semibold text-dark-blue-500 md:text-xl')[0].text
        summary = soup.find_all(class_ = 'py-4 text-justify text-lg font-semibold md:text-xl')[0].text
        
        embed = Embed(title= f'**[{date}] {title}**', description= f'제목을 클릭 시 패치노트를 확인하실 수 있습니다!\n', url= await get_patchnote_link(), colour= 0xFF0055)
        embed.set_author(name= 'ASPHALT 9 : LEGENDS', icon_url= 'https://asphalt9.assets.gameloft.com/assets/a9_logo_12de60294a.png', url= 'https://asphaltlegends.com/')
        embed.set_footer(text= f'{await get_UTC()} (UTC)')
        embed.add_field(name= '< 요약 >', value= f'{summary}\n-----------------------------------', inline= False)
        elements = soup.find('div', class_ = p_tags)
        
            
        if elements:
            if len(elements) > 1000:
                embed.add_field(name= '경고', value= '패치노트가 너무 길어 다 보여줄 수 없습니다. 직접 확인해주세요!')
                return embed
            
            for tag in elements.children:
                    
                if tag.name == 'ul':
                    for tag_children in tag.children:
                        embed.add_field(name= '', value=f'* {tag_children.get_text(strip = True)}\n', inline= False)
                        
                if tag.name == 'h3':
                    embed.add_field(name= f'# {tag.get_text(strip = True)}', value='', inline= False)


    
        
        return embed
    
    else:
        return None