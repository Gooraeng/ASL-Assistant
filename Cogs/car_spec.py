# 차량의 디테일한 성능을 알려주는 명령어
# Last update : 231026

import discord
import typing
import asyncio

from discord.ext import commands
from discord import app_commands
from .utils import manage_tool
from .utils.manage_tool import AboutCar as AC

class spec(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
  
    # 명령어 설명
    @app_commands.command(name='spec', description='차량의 성능을 확인합니다! 이 기능은 외부 데이터에 의해 작동되므로 언제든지 비활성화 될 수 있습니다.')
    @app_commands.describe(car_name='차량 성능 확인')
    @app_commands.rename(car_name='car')
    async def car(self, interaction : discord.Interaction, car_name : str):
        get_check_list = await manage_tool.check_update()
        
        if get_check_list == None:
            get_check_list_ = '없음'
        else:
            get_check_list_ = ('\n* ').join(s for s in get_check_list)
        
        
        embed1 = discord.Embed(title='⚠️주의', description=f'정보가 누락되거나 정확하지 않을 수 있습니다. 문제 발견 시 ASL Assistant 디스코드 서버를 통해 신고해주십시오! (/link 입력)', colour=0x7fe6e4)
        embed1.add_field(name='',value='All list From "MEI Car list", All images from "A9-Database". Type "Ref" For details. ', inline=False)
        embed1.add_field(name='',value='')
        embed1.add_field(name='- 조회 불가능 차량', value= f"* {get_check_list_}", inline= False)
        
        print('---------------------------------------') 
        try:
            if car_name == 'KTM  X-BOW GTX':
                await interaction.response.send_message('', embed=embed1, file=discord.File(f'Car_spec_img/KTM X-BOW GTX.png'),ephemeral=True)
                
            else:
                await interaction.response.send_message('', embed=embed1, file=discord.File(f'Car_spec_img/{car_name}.png'),ephemeral=True)
            print(f"정상 실행 > spec > 실행자: {interaction.user} > 검색 차량 : {car_name}")
        
        # 파일이 존재하지 않음
        except Exception:
            if FileNotFoundError:
                if car_name in get_check_list:
                    embed2 = discord.Embed(title='❗오류', description=f'< {car_name} >의 정보가 현재 없습니다. 조회 불가능한 차량 리스트를 보고 다시 시도해주세요!', colour= 0xff0000)
                    embed2.add_field(name='- 조회 불가능 차량', value=f"* {get_check_list_}", inline= False)
                    embed2.add_field(name='',value='**<경고>** 이 메세지는 20초 뒤에 지워집니다!', inline=False)
                    await interaction.response.send_message('', embed= embed2, ephemeral= True, delete_after=20)
                    print(f'오류 > spec > 실행자: {interaction.user} > 정보가 없는 차량 " {car_name} "" 검색')
                
                else:
                    embed3 = discord.Embed(title='❗오류', description=f'그런 이름의 차량은 없습니다. 다시 시도해주세요!', colour= 0xff0000)
                    embed3.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)
                    await interaction.response.send_message('', embed= embed3, ephemeral= True, delete_after=10)
                    print(f'오류 > spec > 실행자: {interaction.user} > 리스트에 없는 값 " {car_name} "> 입력')
            else:
                embed4 = discord.Embed(title='❗오류', description=f'지금은 조회할 수 없습니다! 잠시 후에 다시 시도해주세요.',colour=0xff0000)
                await interaction.response.send_message('', embed= embed4, ephemeral= True, delete_after=10)
                
                print(f"오류 > spec > 실행자: {interaction.user} > 정보 조회 실패")
                
    # 리스트 자동 완성 
    @car.autocomplete("car_name")
    async def car_autocompletion(self,
        interaction : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
    
        # Choice 리스트 제작을 위한 함수 실행
        new_data = await AC.utilize_list()
        
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