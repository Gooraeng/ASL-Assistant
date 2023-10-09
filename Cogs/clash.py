import discord
from discord.ext import commands
from discord import app_commands
import typing

import numpy
import csv


class clash(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    @app_commands.command(name='clash', description='클럽 클래시 지역의 맵의 레퍼런스를 확인할 수 있습니다!')
    @app_commands.describe(area = '찾고자 하는 맵을 찾아보세요!', car_class = '클래스를 선택하세요', car_name ='어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(area = '맵', car_class = '클래스', car_name = '차량')
    async def clashes(self, interaction: discord.Interaction, area : str, car_class : str, car_name : str):
        # 맵과 차량이 다같이 대응되는 유튜브 링크 제공.
        # 필요한 것 맵 리스트, 차량 리스트, 차량 리스트 안에 링크 append
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
            await interaction.response.send_message('',embed=embed2,ephemeral=True)
    
    @clashes.autocomplete('area')
    async def area_autocompletion(
        self,
        interaciton : discord.Interaction,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        
        a = await database.ClubClash_Database_area()
        map_list = list(set(a))
        result1 = [
            app_commands.Choice(name=choice, value=choice)
            for choice in map_list if current.lower() in choice.lower()
        ]
    
        if len(result1) > 10:
            result1 = result1[:10]
            return result1
        elif current.lower() == '':
            result1 == None
            return result1 
        
    
    @clashes.autocomplete('car_class')
    async def class_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        map_data = await database.ClubClash_Database_area()
        class_data = await database.ClubClash_Database_Class()
        aa = list(interaction.namespace.__dict__.values())
        rest_list = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
        emp_list = list()
        
        for i in range(len(rest_list)):
            emp_list.append(class_data[rest_list[i]])
        
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in list(set(emp_list)) if current.lower() in choice.lower()
        ]
        
        return result2
            
    @clashes.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str, 
    ) -> typing.List[app_commands.Choice[str]]:
        
        # club clash database row 1
        car_data = await database.ClubClash_Database_CarName()
        
        # club clash database row 2
        class_data = await database.ClubClash_Database_Class()
        
        # club clash database 0
        map_data = await database.ClubClash_Database_area()
        
        aa = list(interaction.namespace.__dict__.values())

        # extract area numbers in map_ data list
        rest_list_1 = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
        # make a empty list that will contain car_data name list by using and matching -
        # rest_list's area number.
        # Car_data's length and map_data's one are same so you do not have to mind it.
        emp_list_1 = list()
        emp_list_2 = list()
        for i in range(len(rest_list_1)):
            emp_list_1.append(class_data[rest_list_1[i]])
        
        for i in range(len(rest_list_1)):
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
        
    
class database(): 
    async def ClubClash_Database():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
        data.pop(0)
        f.close()
        return data

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
    
    async def ClubClash_Database_Link():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[3])
        data.pop(0)
        f.close()
        return data
    
async def setup(app):
    await app.add_cog(clash(app))