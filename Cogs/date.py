# 차량의 디테일한 성능을 알려주는 명령어
# Last update : 231017

import discord
from discord import app_commands
from discord.ext import commands

class date(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    @app_commands.command(name='date', description='향후 일정을 확인하실 수 있습니다!')
    @app_commands.guild_only()
    async def show_nengmyeon_bab(self, interaction : discord.Interaction):
        embed = discord.Embed(title='**<주의>**', description='* 일정이 정확하지 않을 수 있으니, 그저 참고만 해주세요!',colour=0xff0000)
        embed.add_field(name= '', value='')
        embed.add_field(name= '- 기간', value= '* 230927 ~ 231219', inline= False)
        
        await interaction.response.send_message('', embed = embed, ephemeral = True, file = discord.File('./images/datesheet.png'))        
        print(f"정상 실행 > date > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}")
        
async def setup(app):
    await app.add_cog(date(app))