# 차량의 디테일한 성능을 알려주는 명령어
# Last update : 231026

import discord
from discord.ext import commands
from discord import app_commands
import typing
from .utils import manage_tool
from .utils.manage_tool import AboutCar as AC
import asyncio

class spec(commands.Cog):
    def __init__(self, app):
        self.app = app
  
    # 명령어 설명
    @app_commands.command(name='spec', description='차량의 성능을 확인합니다! 이 기능은 외부 데이터에 의해 작동되므로 언제든지 비활성화 될 수 있습니다.')
    @app_commands.describe(car_name='차량 성능 확인')
    @app_commands.rename(car_name='car')
    async def car(self, interaction : discord.Interaction, car_name : str):
        get_check_list = await manage_tool.check_update()
        
        if get_check_list == None:
            get_check_list = '없음'
        else:
            get_check_list = (' / ').join(s for s in get_check_list)
        
        
        # Configure/manage_data.py 84 ~ 94번째 줄 참고
        if car_name == 'KTM  X-BOW GTX':
            await interaction.response.send_message('', embed=embed, file=discord.File(f'Car_spec_img/KTM X-BOW GTX.png'),ephemeral=True)
        else:
            embed = discord.Embed(title='주의', description='정보가 누락되거나 정확하지 않을 수 있습니다. 문제 발견 시 ASL Bot 디스코드 서버를 통해 신고해주십시오! (/link 입력)')
            embed.add_field(name='**<경고>**',value='All list From "MEI Car list", All images from "A9-Database". Type "Ref" For details. ', inline=False)
            embed.add_field(name='',value='')
            embed.add_field(name='조회 불가능 차량', value= get_check_list, inline= False)
            try:
                await interaction.response.send_message('', embed=embed, file=discord.File(f'Car_spec_img/{car_name}.png'),ephemeral=True)
            # 파일이 존재하지 않음
            except FileNotFoundError:
                embed1 = discord.Embed(title='오류', description='찾고자 하는 차량의 정보가 없습니다. 나중에 다시 시도해주세요!')
                embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤 지워집니다!', inline=False)
                await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
            except (app_commands.errors.CommandInvokeError, discord.errors.NotFound):
                await interaction.response.defer(ephemeral= True)
                await asyncio.sleep(4)
                await interaction.followup.send('', embed= embed, file= discord.File(f'Car_spec_img/KTM X-BOW GTX.png'),ephemeral=True)
            
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