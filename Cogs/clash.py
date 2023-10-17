# 클럽 클래시 관련 함수
# Last update : 231017

import discord
from discord.ext import commands
from discord import app_commands
import typing
import numpy
import csv
import settings


class database(): 
    
    async def ClubClash_Database_area():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0])
        data.pop(0)
        f.close()
        return data

    async def ClubClash_Database_CarName():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[1])
        data.pop(0)
        f.close()
        return data

    async def ClubClash_Database_Class():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        data.pop(0)
        f.close()
        return data
    
    async def ClubClash_Database_LapTime():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        data.pop(0)
        f.close()
        return data
    
    async def ClubClash_Database_Link():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[4])
        data.pop(0)
        f.close()
        return data
    
class clash(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    @app_commands.command(name='clash', description='클럽 클래시 지역의 맵의 레퍼런스를 확인할 수 있습니다!')
    @app_commands.describe(area = '찾고자 하는 맵을 찾아보세요!', car_class = '클래스를 선택하세요', car_name ='어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(area = '맵', car_class = '클래스', car_name = '차량')
    async def clashes(self, interaction: discord.Interaction, area : str, car_class : str, car_name : str):
        
        # 맵과 차량이 다같이 대응되는 유튜브 링크 제공.
        map_data = await database.ClubClash_Database_area()
        car_data = await database.ClubClash_Database_CarName()
        link_data = await database.ClubClash_Database_Link()
        
        database1 = numpy.array(map_data)
        database2 = numpy.array(car_data)
            
        a = numpy.where(database1 == area)
        b = numpy.where(database2 == car_name)
        
        same = int(numpy.intersect1d(a, b))
        
        
        await interaction.response.send_message(f'{link_data[same]}')
        
        if link_data[same] == False:
            embed2 = discord.Embed(title="경고", description='데이터를 찾을 수 없습니다')
            await interaction.response.send_message('',embed=embed2, ephemeral=True, delete_after=7)
    
    @clashes.autocomplete('area')
    async def area_autocompletion(
        self,
        interaciton : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 차량 리스트 선언
        map_data = await database.ClubClash_Database_area()
        
        # cc_db 내 겹치는 차량 리스트가 존재하고, 리스트 검색 시 이를 허용하지 않게 하기 위한
        # set을 이용하여 겹치는 차량이 없는 새 리스트 선언
        filtered = list(set(map_data))
        
        result1 = [
            app_commands.Choice(name=choice, value=choice)
            for choice in filtered if current.lower() in choice.lower()
        ]
    
        if len(result1) > 10:
            result1 = result1[:10]
        return result1 
        
    
    @clashes.autocomplete('car_class')
    async def class_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str,    
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await database.ClubClash_Database_area()
        class_data = await database.ClubClash_Database_Class()
        
        # area_autocompletion을 통해 찾으려는 맵과 관련된 요소를 불러옴.
        # 여기선 딕셔너리를 이용하여 불러옴 >> dict_values(['Sacred Heart', ''])
        # 리스트로 변환
        aa = list(interaction.namespace.__dict__.values())

        
        # 검색된 맵의 행들을 인덱스로 가지는 리스트를 선언함
        # 이 때, map_data와 aa의 value가 일치하도록 필터링 (aa[0])
        rest_list = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
        
        
        emp_list = list()
        for i in range(len(rest_list)):
            emp_list.append(class_data[rest_list[i]])
        
        # emp_list 내 존재하는 중복 요소 제거
        filetered = list(set(emp_list))
        
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in filetered if current.lower() in choice.lower()
        ]
        
        return result2
            
    @clashes.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str, 
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await database.ClubClash_Database_area()
        car_data = await database.ClubClash_Database_CarName()
        class_data = await database.ClubClash_Database_Class()
        
        # class_autocompletion의 결과와 연동이 어려워 같은 방법 반복
        aa = list(interaction.namespace.__dict__.values())
        rest_list_1 = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
        
        emp_list_1 = list(); emp_list_2 = list()
        
        for i in range(len(rest_list_1)):
            emp_list_1.append(class_data[rest_list_1[i]])
            if class_data[rest_list_1[i]]== str(aa[1]):
                emp_list_2.append(car_data[rest_list_1[i]])
                
        # so, you can check the emp_list.
        result3 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in emp_list_2 if current.lower() in choice.lower()
        ]
        
        if len(result3) > 25:
            result3 = result3[:25]
            
        return result3
        
    
async def setup(app):
    await app.add_cog(clash(app))