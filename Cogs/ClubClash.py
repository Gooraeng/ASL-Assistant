# 클럽 클래시 관련 명령어
# Last Update : 231115

import discord
import typing
import numpy

from discord.ext import commands
from discord import app_commands
from .utils.manage_tool import ClubClash as CC
from .utils import settings, print_time
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

class Clash(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app

    
    @app_commands.command(name='클크', description='클럽 클래시 지역의 맵의 레퍼런스를 확인할 수 있습니다!')
    @app_commands.describe(area = '찾고자 하는 맵을 찾아보세요!', car_class = '클래스를 선택하세요', car_name ='어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(area = '맵', car_class = '클래스', car_name = '차량')
    @app_commands.guilds(751643570758484038, 1151082666670706758)
    @app_commands.guild_only()
    async def clashes(self, interaction: discord.Interaction, area : str, car_class : str, car_name : str):

        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
 
        # ./utils/manage_tool.py 참고
        map_data = await CC.Area_db()
        class_data = await CC.Class_db()
        car_data = await CC.CarName_db()
        link_data = await CC.Link_db()
        lap_time_data = await CC.LapTime_db()
        
        area_arr = numpy.array(map_data); car_name_arr = numpy.array(car_data)
        area_search = numpy.where(area_arr == area); car_name_search = numpy.where(car_name_arr == car_name)
        
        # 임베드 1 선언 (오류)
        embed1 = discord.Embed(title= '어이쿠!', description= f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour=0xff0000)
        embed1.add_field(name='입력 값', value= f'{area} / {car_class} / {car_name}', inline=False)    
        embed1.add_field(name='', value= '**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)    
        
        ch = self.app.get_channel(log_channel)       
        
        log_embed_error = discord.Embed(title= '오류', description= f'클크', colour= failed)
        log_embed_error.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
        log_embed_error.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
        log_embed_error.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
        log_embed_error.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
        log_embed_error.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
        log_embed_error.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
        log_embed_error.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
         
        # veri - asl assistant or asl assistant
        if interaction.channel.id == 1158477800504836147 or interaction.channel.id == 1158749682642714695 or interaction.channel.id == 1168905892469682177:
            same2 = int(numpy.intersect1d(area_search, car_name_search))
            
            try:
                
                # 정상 실행
                if same2 and (car_class in set(class_data)):
                    await interaction.response.send_message(f'```차량 : {car_data[same2]}\n맵   : {map_data[same2]}\n기록 : {lap_time_data[same2]}```\n{link_data[same2]}')
                    
                    confirm = f"정상 실행 > {await print_time.get_UTC()} > 클크 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 검색 내용 : {area} / {car_class} / {car_name}"
                    
                    log_embed = discord.Embed(title= '정상 실행', description= f'클크', colour= etc)
                    log_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
                    log_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
                    log_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
                    log_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
                    log_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
                    log_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
                    log_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
                    log_embed.add_field(name='입력 값' , value= f'{area} / {car_class} / {car_name}', inline= False)
                    
                    await ch.send(embed= log_embed)
                    print(confirm)

                # 임베드 1 출력

                else:
                    await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
                    log_embed_error.add_field(name= f'리스트에 없는 값 입력 ({e})' , value= f'{area} / {car_class} / {car_name}', inline= False)
        
                    no_list = f"오류 > {await print_time.get_UTC()} > 클크 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {area} / {car_class} / {car_name}"
                    await ch.send(embed= log_embed_error)
                    
                    print('---------------------------------------') 
                    print(no_list)
                    print('---------------------------------------') 
            
            # 오류 관리 - 임베드 1 출력 
            except Exception as e:
                await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
                
                log_embed_error.add_field(name= f'리스트에 없는 값 입력 ({e})' , value= f'{area} / {car_class} / {car_name}', inline= False)
        
                no_list = f"오류 > {await print_time.get_UTC()} > 클크 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {area} / {car_class} / {car_name}"
                await ch.send(embed= log_embed_error)
                
                print('---------------------------------------')
                print(no_list)
                print('---------------------------------------')   
        
        else:   
            embed2 = discord.Embed(title= '해당 채널에서는 실행하실 수 없습니다.', colour= 0xf51000,
                                    description= 'ASL Assistant 제작자의 승인이 없는 채널은 이용하실 수 없습니다.')
            failed_excute = f"오류 > {await print_time.get_UTC()} > 클크 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 허가되지 않은 서버 / 채널에서의 명령어 입력"
            
            log_embed_error.add_field(name='실행할 수 없는 서버 / 채널에서 실행' , value= '', inline= False)
            await ch.send(embed= log_embed_error)
            
            print('---------------------------------------')
            print(failed_excute)
            print('---------------------------------------')   
            await interaction.response.send_message(embed= embed2, ephemeral= True, delete_after= 10)        

    @clashes.error
    async def clashes_error_handling(self, interaction : discord.Interaction, error : app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandInvokeError):
            pass
        elif isinstance(error, discord.HTTPException):
            pass
        elif isinstance(error, discord.NotFound):
            pass
        else : raise error
        
        
    @clashes.autocomplete('area')
    async def area_autocompletion(
        self,
        interaciton : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 차량 리스트 선언
        map_data = await CC.Area_db()
        
        map_data.pop(0) 
        # 겹치는 차량 리스트가 존재하고, 리스트 검색 시 이를 허용하지 않게 하기 위한
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
        map_data = await CC.Area_db()
        class_data = await CC.Class_db()
        
        map_data.pop(0) ; class_data.pop(0)
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
        map_data = await CC.Area_db()
        car_data = await CC.CarName_db()
        class_data = await CC.Class_db()
        
        map_data.pop(0); car_data.pop(0); class_data.pop(0)
        # class_autocompletion의 결과와 연동이 어려워 같은 방법 반복
        aa = list(interaction.namespace.__dict__.values())
        rest_list_1 = list(filter(lambda x: map_data[x] == str(aa[0]), range(len(map_data))))
        
        
        emp_list_1 = list(); emp_list_2 = list()
        
        for i in range(len(rest_list_1)):
            emp_list_1.append(class_data[rest_list_1[i]])
            
            if class_data[rest_list_1[i]]== str(aa[1]):
                emp_list_2.append(car_data[rest_list_1[i]])
                
        result3 = [
            app_commands.Choice(name=choice,value=choice)
            for choice in emp_list_2 if current.lower() in choice.lower()
        ]
        
        if len(result3) > 25:
            result3 = result3[:25]
            
        return result3
    
    
            
async def setup(app: commands.Bot):
    await app.add_cog(Clash(app))
    await app.tree.sync(guild = discord.Object(1151082666670706758))
    await app.tree.sync(guild = discord.Object(751643570758484038))