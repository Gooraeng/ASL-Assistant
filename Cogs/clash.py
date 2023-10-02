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
    @app_commands.describe(area = '맵', car_name ='차량')
    @app_commands.rename(area = '맵', car_name = '차량')
    
    async def clash(self, interaction: discord.Interaction, area : str, car_name : str):
        # 맵과 차량이 다같이 대응되는 유튜브 링크 제공.
        # 필요한 것 맵 리스트, 차량 리스트, 차량 리스트 안에 링크 append
        map_data = await database.ClubClash_Database_area()
        car_data = await database.ClubClash_Database_CarName()
        link_data = await database.ClubClash_Database_Link()
        database1 = numpy.array(map_data)
        database2 = numpy.array(car_data)
        a = numpy.where(database1 == area)
        b = numpy.where(database2 == car_name)
        same=int(numpy.intersect1d(a,b))
        await interaction.response.send_message(f"{link_data[same]}",ephemeral=True)
        
    
    @clash.autocomplete('area')
    async def area_autocompletion(
        self,
        interaciton : discord.Interaction,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 맵 리스트..
        a = await database.ClubClash_Database_area()
        map_list = list(set(a))
        result1 = [
            app_commands.Choice(name=choice, value=choice)
            for choice in map_list if current.lower() in choice.lower()
        ]
        if len(result1) > 10:
            result1 = result1[:10]
        return result1
        
    @clash.autocomplete('car_name')
    async def car_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str, 
    ) -> typing.List[app_commands.Choice[str]]:
        a = await database.ClubClash_Database_CarName()
        new_list = list(set(a))
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in new_list if current.lower() in choice.lower()
            ]
        if len(result2) > 10:
            result2 = result2[:10]
        return result2
    
        
async def setup(app):
    await app.add_cog(clash(app))



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

    async def ClubClash_Database_Link():
        data = list()
        f = open('data/Club Clash Database.csv', "r",encoding='utf-8',newline='')
        reader = csv.reader(f)
        for row in reader:
            data.append(row[2])
        data.pop(0)
        f.close()
        return data