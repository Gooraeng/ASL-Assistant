# 차량 및 크럽 클래시
# Last Update : 231115

import discord
import typing

from discord.ext import commands
from discord import app_commands
from .utils import settings, print_time
from .utils.manage_tool import CarhuntRiot as CR
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

class car_hunt(commands.Cog):
    
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
    
    
    @app_commands.command(name='car-hunt', description= '카헌트 영상을 보여줍니다!')
    @app_commands.describe(car = '어떤 차량을 고르시나요?')
    @app_commands.guild_only()
    async def car_hunt_search(self, interaciton : discord.Interaction, car : str):

        if interaciton.channel.id == log_channel or interaciton.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaciton)

        else:
            car_data = await CR.CarName_db()
            map_data = await CR.Area_db()
            lap_time_data = await CR.LapTime_db()
            link_data = await CR.Link_db()
            
            ch = self.app.get_channel(log_channel)
            
            try:            
                CarName_found = car_data.index(car)
            
                await interaciton.response.send_message(f'```차량 : {car_data[CarName_found]}\n\
                                                            맵 : {map_data[CarName_found]}\n\
                                                            기록 : {lap_time_data[CarName_found]}```\n\
                                                            {link_data[CarName_found]}')
                
                log_embed = discord.Embed(title= '정상 실행', description= f'car hunt', colour= etc)
                log_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
                log_embed.add_field(name='서버명', value= f'{interaciton.guild.name}', inline= True)
                log_embed.add_field(name='채널명', value= f'{interaciton.channel.name}', inline= True)
                log_embed.add_field(name='유저', value= f'{interaciton.user.display_name}', inline= True)
                log_embed.add_field(name='서버 ID', value= f'{interaciton.guild.id}', inline= True)
                log_embed.add_field(name='채널 ID', value= f'{interaciton.channel.id}', inline= True)
                log_embed.add_field(name='유저 ID', value= f'{interaciton.user.id}', inline= True)
                log_embed.add_field(name='입력 값' , value= f'{car}', inline= False)
                    
                confirm = f"정상 실행 > {await print_time.get_UTC()} > car-hunt > 서버: {interaciton.guild.name} > 채널 : {interaciton.channel.name} > 실행자: {interaciton.user.display_name} > 검색 차량 : {car}"
                await ch.send(embed= log_embed); print(confirm)
            
            except Exception:
                embed1 = discord.Embed(title='❗오류', description=f'< {car} >의 정보가 없습니다. 다시 시도해주세요!', colour= 0xff0000)
                embed1.add_field(name='',value='**<경고>** 이 메세지는 20초 뒤에 지워집니다!', inline=False)
                
                await interaciton.response.send_message('', embed= embed1, ephemeral= True, delete_after=20)
            
                log_embed_error = discord.Embed(title= '오류', description= f'car hunt', colour= failed)
                log_embed_error.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
                log_embed_error.add_field(name='서버명', value= f'{interaciton.guild.name}', inline= True)
                log_embed_error.add_field(name='채널명', value= f'{interaciton.channel.name}', inline= True)
                log_embed_error.add_field(name='유저', value= f'{interaciton.user.display_name}', inline= True)
                log_embed_error.add_field(name='서버 ID', value= f'{interaciton.guild.id}', inline= True)
                log_embed_error.add_field(name='채널 ID', value= f'{interaciton.channel.id}', inline= True)
                log_embed_error.add_field(name='유저 ID', value= f'{interaciton.user.id}', inline= True)
                log_embed_error.add_field(name='리스트에 없는 값 입력' , value= f'{car}', inline= False)
                
                no_list = f"오류 > {await print_time.get_UTC()} > car-hunt > 서버: {interaciton.guild.name} > 채널 : {interaciton.channel.name} > 실행자: {interaciton.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {car}"
                await ch.send(embed= log_embed_error)
                
                print('---------------------------------------') 
                print(no_list)
                print('---------------------------------------')
            
        
    @car_hunt_search.autocomplete('car')
    async def chs_autocpletion(self,
        interaction : discord.Interaction,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        
        car_name = await CR.CarName_db()
        
        result = [
            app_commands.Choice(name= choice, value= choice)
            for choice in car_name if current.lower() in choice.lower()
        ]
        
        if len(result) > 10:
            result = result[:10]
            
        return result

async def setup(app):
    await app.add_cog(car_hunt(app))
        