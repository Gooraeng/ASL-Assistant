# 차량의 디테일한 성능을 알려주는 명령어

import discord
from discord.ext import commands
from discord import app_commands
import csv
import typing
import os

import requests as req
from bs4 import BeautifulSoup as beau
import pandas as pd
import settings


# A9 차량 리스트 관련 파일 임포트


class spec(commands.Cog):
    def __init__(self, app):
        self.app = app
  
    # 명령어 설명
    @app_commands.command(name='spec', description='차량의 성능을 확인합니다! 이 기능은 외부 데이터에 의해 작동되므로 언제든지 비활성화 될 수 있습니다.')
    @app_commands.describe(car_name='차량 성능 확인')
    @app_commands.rename(car_name='car')
    async def car(self, interaction : discord.Interaction, car_name : str):
        embed = discord.Embed(title='주의', description='정보가 누락되거나 정확하지 않을 수 있습니다. 문제 발견 시 /link를 입력 후 보이는 링크를 통해 신고해주십시오!')
        embed.add_field(name='**<경고>**',value='All list From "MEI Car list", All images from "A9-Database". Type "Ref" For details. ', inline=False)
        
        # car_list.py 76째 줄 참고
        if car_name == 'KTM  X-BOW GTX':
            await interaction.response.send_message('', embed=embed, file=discord.File(f'{settings.car_img}/KTM X-BOW GTX.png'),ephemeral=True)
        else:
            try:
                await interaction.response.send_message('', embed=embed, file=discord.File(f'{settings.car_img}/{car_name}.png'),ephemeral=True)
            # 파일이 존재하지 않음
            except FileNotFoundError:
                embed1 = discord.Embed(title='오류', description='찾고자 하는 차량의 정보가 없습니다. 나중에 다시 시도해주세요!')
                embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤 지워집니다!', inline=False)
                await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
                
            
    # 리스트 자동 완성 
    @car.autocomplete("car_name")
    async def car_autocompletion(self,
        interaction : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
    
        # Choice 리스트 제작을 위한 함수 실행
        new_data = await manage.utilize_list()
        
        # Choice 갯수가 10개 초과 시 최대로 보여주는 Choice 수를 10개 까지로 제한
        result = [
            app_commands.Choice(name= choice, value= choice)
            for choice in new_data if current.lower() in choice.lower()
        ]
        if len(result) > 10:
                result = result[:10]
        return result

async def setup(app):
    await app.add_cog(spec(app))
    

# 사이트로부터 리스트 정보 받아오기
class manage():
    async def make_new_car_list():
        url = settings.list_url
    
        response = req.get(url).text.encode('utf-8')
        response = beau(response, 'lxml')
    
        target = response.find('table',{'id':'list', 'class':'table'})
        thead = target.find_all('th')
    
        theadList = []

    # 사이트 내 th, td 태그 제거 
        theadLen = len(thead)
        for i in range(0, theadLen):
            thead = target.find_all('th')[i].text
            theadList.append(thead)

        tdTags = target.find_all('td')

        rowList=[]
        columnList = []

        tdTagsLen = len(tdTags)
        for i in range(0, tdTagsLen):
            element = tdTags[i].text
            columnList.append(element)
            if i % 2 ==1:
                rowList.append(columnList)
                columnList=[]
        result = pd.DataFrame(rowList, columns=theadList)
    # 태그 제거 결과 확인
        print(result)
    
    # csv 파일로 우선 저장 [차량, 클래스] 꼴로 저장됨
        f = open(settings.car_list,'w',encoding='utf-8',newline='')
        writer = csv.writer(f)
        writer.writerow(theadList)
        writer.writerows(rowList)
        f.close()
        
# make_new_car_list에서 나온 [차량, 클래스 중] [차량]만 활용할 수 있게 csv 파일 편집 
    async def utilize_list():
        data = list()
        f = open(settings.car_list, "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        data.pop(0)
        f.close()
        return data

# 차량 사진 리스트 추출 및 csv 파일 간 대조
    async def check_update():  
        data = await manage.utilize_list()  
        car_img_list = list()
        for filename in os.listdir(settings.car_img):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                car_img_list.append(filename[:-4])
            elif filename.endswith(".jpeg"):
                car_img_list.append(filename[:-5])
    
    # 업데이트 된 차량(들)의 리스트 선언 
        check_new = list(set(data)- set(car_img_list))

    # 리스트 대조 후 일치 시
    # KTM X-BOW GTX는 이미 존재하는 차량인데 data 리스트에서는 띄어쓰기가 두 번 적용된 것이 확인되어 억지로 맞게 만듬
        if len(list(data))-len(list(car_img_list))==0:
            if 'KTM  X-BOW GTX' in data:
                print('추가된 차량이 없습니다!')

    # 리스트 대조 후 불일치 시
    # 76번 줄과 같은 사유
        else:
            if 'KTM  X-BOW GTX' in data:
                check_new.remove('KTM  X-BOW GTX')
                print('차량 업데이트 발견: '+ str(check_new))