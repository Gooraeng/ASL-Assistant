# 클럽 클래시 관련 명령어
# Last Update : 231107

import discord
import typing
import numpy

from discord.ext import commands
from discord import app_commands
from .utils.manage_tool import TimeLimitedEvent as TimeLE
from .utils import settings, print_time

log_channel = int(settings.log_channel)


class tle(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
        
    @app_commands.command(name='tle', description='주간 경쟁, 엘리트컵부터 다른 TLE까지 알려드립니다!')
    @app_commands.describe(tle_type = '어떤 TLE 타입인가요?', area = '맵을 고르세요!', car_name ='어떤 차량을 찾아보시겠어요?')
    @app_commands.rename(tle_type = '타입', area = '맵', car_name = '차량')
    @app_commands.guild_only()
    async def TimeLEs(self, interaction: discord.Interaction, tle_type : str, area : str, car_name : str):

        # ./utils/manage_tool.py 참고
        tle_data = await TimeLE.type_of_tle()
        map_data = await TimeLE.Area_db()
        car_data = await TimeLE.CarName_db()
        
        lap_time_data = await TimeLE.LapTime_db()
        link_data = await TimeLE.Link_db()
        
        map_arr = numpy.array(map_data)
        car_arr = numpy.array(car_data)
            
        b = numpy.where(map_arr == area)
        c = numpy.where(car_arr == car_name)
        
        # 임베드 1 선언 (오류)
        embed1 = discord.Embed(title='어이쿠!', description=f'무언가 잘못되었습니다. 잠시 후에 다시 시도해주세요.',colour=0xff0000)
        embed1.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤에 지워집니다!', inline=False)    
        
        ch = self.app.get_channel(log_channel)        
        
        try:
            same2 = int(numpy.intersect1d(b, c))
            
            # 정상 실행
            if same2 and (tle_type in set(tle_data)):
                await interaction.response.send_message(f'## 기록 : {lap_time_data[same2]} \n\n{link_data[same2]}')
                
                confirm = f"정상 실행 > {await print_time.get_UTC()} > tle > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 검색 내용 : {tle_type} / {area} / {car_name}"
                await ch.send(confirm); print(confirm)

            # 임베드 1 출력
            else:
                await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
                
                no_list = f"오류 > {await print_time.get_UTC()} > tle > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {tle_type} / {area} / {car_name}"
                await ch.send(no_list)
                
                print('---------------------------------------') 
                print(no_list)
                print('---------------------------------------') 
        
        # 오류 관리 - 임베드 1 출력 
        except Exception:
            await interaction.response.send_message('', embed= embed1, ephemeral= True, delete_after=10)
            
            no_list = f"오류 > {await print_time.get_UTC()} > tle > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 리스트에 없는 값 입력 > 입력 내용 : {tle_type} / {area} / {car_name}"
            await ch.send(no_list)
            
            print('---------------------------------------')
            print(no_list)
            print('---------------------------------------') 
            
    @TimeLEs.autocomplete(name= 'tle_type')
    async def tle_type_autocompletion(
        self,
        interaciton : discord.Interaction,
        current : str,
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 차량 리스트 선언
        tle_type_data = await TimeLE.type_of_tle()
        
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
        
    
    @TimeLEs.autocomplete(name= 'area')
    async def area_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str,    
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        tle_type_data = await TimeLE.type_of_tle()
        map_data = await TimeLE.Area_db()
        
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
            
    @TimeLEs.autocomplete(name='car_name')
    async def car_autocompletion(
        self,
        interaction : discord.Interaction,
        current : str, 
    ) -> typing.List[app_commands.Choice[str]]:
        
        # 리스트 선언
        tle_type_data = await TimeLE.type_of_tle()
        map_data = await TimeLE.Area_db()
        car_data = await TimeLE.CarName_db()
        
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
    await app.add_cog(tle(app))