# 클럽 클래시 관련 명령어
# Last Update : 231115

import discord
import typing
import numpy

from discord.ext import commands
from discord import app_commands
from .utils.manage_tool import WeeklyCompetition as WC
from .utils import settings, print_time
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

class WeeklycompetionKR(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
    @app_commands.command(name= '주경', description= '주간 경쟁 레퍼런스를 보여드립니다!')
    @app_commands.describe(area= '맵을 고르세요!', car_name= '어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(area= '맵', car_name= '차량')
    @app_commands.guild_only()
    async def weeklycompete(self, interaction: discord.Interaction, area : str, car_name : str):
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        # ./utils/manage_tool.py 참고
        
        map_data = await WC.Area_db()
        car_data = await WC.CarName_db()
        lap_time_data = await WC.LapTime_db()
        link_data = await WC.Link_db()
        
        map_arr = numpy.array(map_data)
        car_arr = numpy.array(car_data)
            
        map_arr_where = numpy.where(map_arr == area)
        car_arr_where = numpy.where(car_arr == car_name)
        
        # 임베드 1 선언 (오류)
        embed1 = discord.Embed(title='어이쿠!', description=f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour=0xff0000)
        embed1.add_field(name= '검색', value= f'{area} / {car_name}')
        embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)    
        
        ch = self.app.get_channel(log_channel)        
        
        log_embed_error = discord.Embed(title= '오류', description= f'주경', colour= failed)
        log_embed_error.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
        log_embed_error.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
        log_embed_error.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
        log_embed_error.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
        log_embed_error.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
        log_embed_error.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
        log_embed_error.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
        log_embed_error.add_field(name='리스트에 없는 값 입력' , value= f'{area} / {car_name}', inline= False)
        
        
        same_num_list = int(numpy.intersect1d(map_arr_where, car_arr_where))
        
        # 정상 실행
        if same_num_list:
            await interaction.response.send_message(f'```차량 : {car_data[same_num_list]}\n맵   : {map_data[same_num_list]}\n기록 : {lap_time_data[same_num_list]}```\n{link_data[same_num_list]}')
            
            log_embed = discord.Embed(title= '정상 실행', description= f'주경', colour= etc)
            log_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)        
            log_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
            log_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
            log_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
            log_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
            log_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
            log_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
            log_embed.add_field(name='입력 값' , value= f'{area} / {car_name}', inline= False)
            await ch.send(embed= log_embed)
            
            confirm = f"정상 실행 > {await print_time.get_UTC()} > 주경 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 검색 내용 : {area} / {car_name}"
            print(confirm)

        # 오류(알맞지 않은 입력) - 임베드 1 출력
        else:
            await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
            await ch.send(embed = log_embed_error)
            
            no_list = f"오류 > {await print_time.get_UTC()} > 주경 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {area} / {car_name}"
            print('---------------------------------------') 
            print(no_list)
            print('---------------------------------------') 

            
    @weeklycompete.autocomplete(name= 'area')
    async def area_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str,    
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await WC.Area_db()
        
        map_data.pop(0)
        
        # emp_list 내 존재하는 중복 요소 제거
        filetered = list(set(map_data))
        
        result1 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in filetered if current.lower() in choice.lower()
        ]
        
        if len(result1) > 25:
            result1 = result1[:25]
            
        return result1

            
    @weeklycompete.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str, 
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        map_data = await WC.Area_db()
        car_data = await WC.CarName_db()
        
        map_data.pop(0); car_data.pop(0)

        aa = list(interaction.namespace.__dict__.values())
        
        rest_list = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
         
        emp_list = list()
        for i in range(len(rest_list)):
            emp_list.append(car_data[rest_list[i]])

                
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in emp_list if current.lower() in choice.lower()
        ]
        
        if len(result2) > 25:
            result2 = result2[:25]
            
        return result2
        

    
async def setup(app : commands.Bot):
    await app.add_cog(WeeklycompetionKR(app))