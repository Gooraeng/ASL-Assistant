# 차량 및 크럽 클래시
# Last Update : 231115

import discord
import typing

from discord.ext import commands
from discord import app_commands
from .utils import settings, print_time
from utils.manage_tool import CarhuntRiot as CR
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class CarHunt(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
    
    
    @app_commands.command(name='카헌트', description= '카헌트 영상을 보여줍니다!')
    @app_commands.describe(car = '어떤 차량을 고르시나요?')
    @app_commands.rename(car = '차량')
    @app_commands.guild_only()
    async def car_hunt_search(self, interaciton : discord.Interaction, car : str):

        # 로그 채널에 명령어 입력 시 실행을 막는 임베드 출력
        if interaciton.channel.id == log_channel or interaciton.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaciton)

        else:
            
            car_data = await CR.CarName_db()
            map_data = await CR.Area_db()
            lap_time_data = await CR.LapTime_db()
            link_data = await CR.Link_db()
            
            ch = self.app.get_channel(log_channel)
            
            try:
                # 입력한 차량명과 일치하는 차량의 인덱스 넘버 변수 선언 
                CarName_found = car_data.index(car)
            
                await interaciton.response.send_message(f'```차량 : {car_data[CarName_found]}\n맵   : {map_data[CarName_found]}\n기록 : {lap_time_data[CarName_found]}```\n{link_data[CarName_found]}')
                
                # 정상 실행 로그
                log_embed = discord.Embed(title= '정상 실행', description= f'카헌트', colour= etc)
                log_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
                log_embed.add_field(name='서버명', value= f'{interaciton.guild.name}', inline= True)
                log_embed.add_field(name='채널명', value= f'{interaciton.channel.name}', inline= True)
                log_embed.add_field(name='유저', value= f'{interaciton.user.display_name}', inline= True)
                log_embed.add_field(name='서버 ID', value= f'{interaciton.guild.id}', inline= True)
                log_embed.add_field(name='채널 ID', value= f'{interaciton.channel.id}', inline= True)
                log_embed.add_field(name='유저 ID', value= f'{interaciton.user.id}', inline= True)
                log_embed.add_field(name='입력 값' , value= f'{car}', inline= False)
                await ch.send(embed= log_embed)    
                
                confirm = f"정상 실행 > {await print_time.get_UTC()} > 카헌트 > 서버: {interaciton.guild.name} > 채널 : {interaciton.channel.name} > 실행자: {interaciton.user.display_name} > 검색 차량 : {car}"
                print(confirm)
            
            except Exception:
                
                embed1 = discord.Embed(title='❗오류', description=f'< {car} >의 정보가 없습니다. 다시 시도해주세요!', colour= 0xff0000)
                embed1.add_field(name='',value='**<경고>** 이 메세지는 20초 뒤에 지워집니다!', inline=False)
                
                await interaciton.response.send_message('', embed= embed1, ephemeral= True, delete_after=20)
            
                log_embed_error = discord.Embed(title= '오류', description= f'카헌트', colour= failed)
                log_embed_error.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
                log_embed_error.add_field(name='서버명', value= f'{interaciton.guild.name}', inline= True)
                log_embed_error.add_field(name='채널명', value= f'{interaciton.channel.name}', inline= True)
                log_embed_error.add_field(name='유저', value= f'{interaciton.user.display_name}', inline= True)
                log_embed_error.add_field(name='서버 ID', value= f'{interaciton.guild.id}', inline= True)
                log_embed_error.add_field(name='채널 ID', value= f'{interaciton.channel.id}', inline= True)
                log_embed_error.add_field(name='유저 ID', value= f'{interaciton.user.id}', inline= True)
                log_embed_error.add_field(name='리스트에 없는 값 입력' , value= f'{car}', inline= False)
                await ch.send(embed= log_embed_error)
                
                no_list = f"오류 > {await print_time.get_UTC()} > 카헌트 > 서버: {interaciton.guild.name} > 채널 : {interaciton.channel.name} > 실행자: {interaciton.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {car}"
                print('---------------------------------------') 
                print(no_list)
                print('---------------------------------------')
            
        
    @car_hunt_search.autocomplete('car')
    async def chs_autocpletion(self,
        interaction : discord.Interaction,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        
        car_name = await CR.CarName_db()
        car_name.pop(0)
        
        result = [
            app_commands.Choice(name= choice, value= choice)
            for choice in car_name if current.lower() in choice.lower()
        ]
        
        if len(result) > 10:
            result = result[:10]
            
        return result



async def setup(app):
    await app.add_cog(CarHunt(app))
        