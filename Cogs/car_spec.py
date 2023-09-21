import discord
from discord.ext import commands
from discord import app_commands
import csv
import typing

# A9 차량 리스트 관련 메소드 임포트
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import settings, car_list

class spec(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    
    # read csv files to make a list of choices
    data = list()
    f = open(settings.the_csv, "r",encoding='utf-8')
    reader = csv.reader(f)
    for row in reader:
        data.append(row[0])    



    @app_commands.command(name='spec', description='차량의 성능을 확인합니다!')
    @app_commands.describe(car_name='차량 성능 확인')
    @app_commands.rename(car_name='car')
    async def car(self, interaction : discord.Interaction, car_name : str):
        embed = discord.Embed(title='주의', description='정보가 누락되거나 정확하지 않을 수 있습니다. 문제 발견 시 /link를 입력 후 보이는 링크를 통해 신고해주십시오!')
        if car_name == 'KTM  X-BOW GTX':
            await interaction.response.send_message('', embed=embed, file=discord.File('./Car_spec_img/KTM X-BOW GTX.png'),ephemeral=True)
        else:
            await interaction.response.send_message('', embed=embed, file=discord.File(f'./Car_spec_img/{car_name}.png'),ephemeral=True)
        
    @car.autocomplete("car_name")
    async def car_autocompletion(self,
        interaction : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
        new_data = list(spec.data)
        result = [
            app_commands.Choice(name= choice, value= choice)
            for choice in new_data if current.lower() in choice.lower()
        ]
        if len(result) > 10:
                result = result[:10]
        return result

async def setup(app):
    await app.add_cog(spec(app))