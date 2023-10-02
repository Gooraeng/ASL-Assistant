# 메인 코드 모음

import asyncio
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import settings
import requests as req
from bs4 import BeautifulSoup as beau
import pandas as pd
import csv

intents = discord.Intents.default()
app = commands.Bot(command_prefix="/",intents=intents)

# 확장 기능(명령어) 로드
async def load_extensions():
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            try:
                await app.load_extension(f"Cogs.{filename[:-3]}")            
# 오류 처리
            except (commands.NoEntryPointError, commands.ExtensionFailed):
                print(f"파일 오류 발생 : {filename}")
            except commands.ExtensionNotFound:
                print(f"{filename[:-3]} 파일이 존재하지 않습니다.")
       

# 봇 이벤트
@app.event
async def on_ready():
    await load_extensions()
    await manage.make_new_car_list()
    print('---------------------------------------')
    await manage.check_update()
    print('---------------------------------------')   
    print(f"{app.user.name} 준비 중")
    try:
        synced = await app.tree.sync()
        print(f"명령어 {len(synced)}개 사용 가능")
        current_status = discord.Game(name='A9차량 정보제공')
        await app.change_presence(status=discord.Status.online,activity=current_status)
        print(f"{app.user.name}이(가) 준비되었습니다!")

    # 매일 한 번 씩 차량 리스트 업데이트 실행
        while True:           
            await asyncio.sleep(86400)
            print('---------------------------------------')
            await manage.make_new_car_list()
            await manage.check_update()
            print('갱신 완료')
            
    except Exception as e:
        print(e)
# 에러 관리
async def on_command_error(ctx, interaction : discord.Interaction, error):
    # 존재하지 않는 명령어 에러처리
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="오류",description="존재하지 않는 명령어입니다.",colour=0xFF0000)
        await interaction.response.send_message("",embed=embed,ephemeral=True) 
    
    # 명령어 오류 처리
    else:
        embed = discord.Embed(title="오류",description="예기치 못한 오류가 발생했습니다.",colour=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await interaction.response.send_message("",embed=embed,ephemeral=True)
    
# 사이트로부터 리스트 정보 받아오기
class manage():
    async def make_new_car_list():
        url = 'https://www.mei-a9.info/cars'
    
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
        f = open('data/A9 Car List.csv','w',encoding='utf-8',newline='')
        writer = csv.writer(f)
        writer.writerow(theadList)
        writer.writerows(rowList)
        f.close()
        
# make_new_car_list에서 나온 [차량, 클래스 중] [차량]만 활용할 수 있게 csv 파일 편집 
    async def utilize_list():
        data = list()
        f = open('data/A9 Car List.csv', "r",encoding='utf-8',newline='')
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
        for filename in os.listdir("Car_spec_img"):
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
                
# 메인
app.run(settings.token)