# 클럽 클래시 관련 명령어
# Last Update : 231115

import discord
import typing
import numpy

from discord.ext import commands
from discord import app_commands
from .utils.manage_tool import TimeLimitedEventData as TLED
from .utils import settings, print_time
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

class TLE(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
        
    @app_commands.command(name='tle', description='주간 경쟁, 엘리트컵부터 다른 TLE까지 알려드립니다!')
    @app_commands.describe(tle_type = '어떤 TLE 타입인가요?', area = '맵을 고르세요!', car_name ='어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(tle_type = '타입', area = '맵', car_name = '차량')
    @app_commands.guild_only()
    async def tle(self, interaction: discord.Interaction, tle_type : str, area : str, car_name : str):
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        # ./utils/manage_tool.py 참고
        tle_data = await TLED.type_of_tle()
        map_data = await TLED.Area_db()
        car_data = await TLED.CarName_db()
        lap_time_data = await TLED.LapTime_db()
        link_data = await TLED.Link_db()
        
        map_arr = numpy.array(map_data)
        car_arr = numpy.array(car_data)
            
        map_arr_where = numpy.where(map_arr == area)
        car_arr_where = numpy.where(car_arr == car_name)
        
        # 임베드 1 선언 (오류)
        embed1 = discord.Embed(title='어이쿠!', description=f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour=0xff0000)
        embed1.add_field(name= '검색', value= f'{tle_type} / {area} / {car_name}')
        embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)    
        
        ch = self.app.get_channel(log_channel)        
        
        log_embed_error = discord.Embed(title= '오류', description= f'tle', colour= failed)
        log_embed_error.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
        log_embed_error.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
        log_embed_error.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
        log_embed_error.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
        log_embed_error.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
        log_embed_error.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
        log_embed_error.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
        log_embed_error.add_field(name='리스트에 없는 값 입력' , value= f'{tle_type} / {area} / {car_name}', inline= False)
        
        
        try:
            same_num_list = int(numpy.intersect1d(map_arr_where, car_arr_where))
            
            # 정상 실행
            if same_num_list and (tle_type in set(tle_data)):
                await interaction.response.send_message(f'```차량 : {car_data[same_num_list]}\n맵 : {map_data[same_num_list]}\n기록 : {lap_time_data[same_num_list]}```\n{link_data[same_num_list]}')
                
                log_embed = discord.Embed(title= '정상 실행', description= f'tle', colour= etc)
                log_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)        
                log_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
                log_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
                log_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
                log_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
                log_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
                log_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
                log_embed.add_field(name='입력 값' , value= f'{tle_type} / {area} / {car_name}', inline= False)
                await ch.send(embed= log_embed)
                
                confirm = f"정상 실행 > {await print_time.get_UTC()} > tle > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 검색 내용 : {tle_type} / {area} / {car_name}"
                print(confirm)

            # 오류(알맞지 않은 입력) - 임베드 1 출력
            else:
                await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
                await ch.send(embed = log_embed_error)
                
                no_list = f"오류 > {await print_time.get_UTC()} > tle > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {tle_type} / {area} / {car_name}"
                print('---------------------------------------') 
                print(no_list)
                print('---------------------------------------') 
        
        # 오류(알맞지 않은 입력) - 임베드 1 출력 
        except Exception:
            await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
            await ch.send(embed = log_embed_error)
            
            no_list = f"오류 > {await print_time.get_UTC()} > tle > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {tle_type} / {area} / {car_name}"
            print('---------------------------------------')
            print(no_list)
            print('---------------------------------------') 

            
    @tle.autocomplete(name= 'tle_type')
    async def tle_type_autocompletion(
        self,
        interaciton : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 차량 리스트 선언
        tle_type_data = await TLED.type_of_tle()
        
        tle_type_data.pop(0)
        # 겹치는 TLE Type 리스트가 존재하고, 리스트 검색 시 이를 허용하지 않게 하기 위한
        # set을 이용하여 겹치는 Type이 없는 새 리스트 선언
        filtered = list(set(tle_type_data))
        
        result1 = [
            app_commands.Choice(name=choice, value=choice)
            for choice in filtered if current.lower() in choice.lower()
        ]
    
        if len(result1) > 10:
            result1 = result1[:10]
            
        return result1
        
    
    @tle.autocomplete(name= 'area')
    async def area_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str,    
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        tle_type_data = await TLED.type_of_tle()
        map_data = await TLED.Area_db()
        
        tle_type_data.pop(0); map_data.pop(0)
        # tle_type_autocompletion을 통해 찾으려는 맵과 관련된 요소를 불러옴.
        # 여기선 딕셔너리를 이용하여 불러옴 >> dict_values(['Weekly Competition', ''])
        # 리스트로 변환
        aa = list(interaction.namespace.__dict__.values())
        
        # 검색된 맵의 행들을 인덱스로 가지는 리스트를 선언함
        # 이 때, map_data와 aa의 value가 일치하도록 필터링 (aa[0])
        rest_list = list(filter(lambda x: tle_type_data[x] == str(aa[0]), range(len(tle_type_data))))
           
        emp_list = list()
        for i in range(len(rest_list)):
            emp_list.append(map_data[rest_list[i]])
        
        # emp_list 내 존재하는 중복 요소 제거
        filetered = list(set(emp_list))
        
        result2 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in filetered if current.lower() in choice.lower()
        ]
        
        if len(result2) > 25:
            result2 = result2[:25]
            
        return result2

            
    @tle.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str, 
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        tle_type_data = await TLED.type_of_tle()
        map_data = await TLED.Area_db()
        car_data = await TLED.CarName_db()
        
        tle_type_data.pop(0); map_data.pop(0); car_data.pop(0)
        # class_autocompletion의 결과와 연동이 어려워 같은 방법 반복
        aa = list(interaction.namespace.__dict__.values())
        rest_list_1 = list(filter(lambda x: tle_type_data[x] == str(aa[0]), range(len(tle_type_data))))
         
        emp_list_1 = list(); emp_list_2 = list()
        
        for i in range(len(rest_list_1)):
            emp_list_1.append(map_data[rest_list_1[i]])
            
            if map_data[rest_list_1[i]]== str(aa[1]):
                emp_list_2.append(car_data[rest_list_1[i]])
                
        result3 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in emp_list_2 if current.lower() in choice.lower()
        ]
        
        if len(result3) > 25:
            result3 = result3[:25]
            
        return result3
        

    
async def setup(app : commands.Bot):
    await app.add_cog(TLE(app))