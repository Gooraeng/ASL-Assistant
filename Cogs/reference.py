# car_spec.py의 레퍼런스가 된 자료들의 정보를 알려줌
# Last update : 231017

import discord
from discord.ext import commands
from discord import app_commands

class ref(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    @app_commands.command(name='ref', description='봇의 레퍼런스 및 출처를 알려줍니다.')
    @app_commands.guild_only()
    async def ref(self, interaction : discord.Interaction):
        embed1=discord.Embed(title="레퍼런스 1 - MEI", url='https://www.mei-a9.info/cars', description='클릭 시 링크로 이동합니다.',color=0x7fe6e4)
        embed1.add_field(name="- 사용목적", value="아스팔트 9 차량 리스트 추출")
        
        embed2=discord.Embed(title="레퍼런스 2 - A9 Database", description='클릭 시 링크로 이동합니다.', url='https://discord.gg/dVA7R9CXpB', color=0x7fe6e4)
        embed2.add_field(name="- 사용목적", value="아스팔트 9 차량 스펙 데이터 베이스 활용")
        
        embed3=discord.Embed(title="레퍼런스 3 - A9 Club Clash Database", description='Created by Sharp', color=0x7fe6e4)
        embed3.add_field(name="- 사용목적", value="아스팔트 9 클럽 클래시 데이터 베이스 활용")
        await interaction.response.send_message('', embeds= [embed1, embed2, embed3], ephemeral= True)
        
        print(f"정상 실행 > ref > 서버: {interaction.guild.name} > 실행자: {interaction.user.display_name}")
        
async def setup(app):
    await app.add_cog(ref(app))