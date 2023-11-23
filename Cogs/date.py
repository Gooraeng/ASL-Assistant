# 향후 일정 사진을 출력하는 명령어
# Last Update : 231115

import discord

from discord import app_commands
from discord.ext import commands
from .utils import settings, print_time
from .utils.embed_log import succeed, failed, etc
from .utils.not_here import not_here_return_embed

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class date(commands.Cog):
    def __init__(self, app : commands.Bot):
        self.app = app
    
    
    @app_commands.command(name='date', description='향후 일정을 확인하실 수 있습니다!')
    @app_commands.guild_only()
    async def show_date(self, interaction : discord.Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction)
        
        else:
            embed = discord.Embed(title='**<주의>**', description='* 일정이 정확하지 않을 수 있으니, 그저 참고만 해주세요!',colour=0xff0000)
            embed.add_field(name= '- 기간', value= '* 230927 ~ 231219', inline= False)
            
            await interaction.response.send_message('', embed = embed, ephemeral = True, file = discord.File('./images/datesheet.png'))
                    
            ch = self.app.get_channel(log_channel)
            
            no_variable_embed = discord.Embed(title= '정상 실행', description= f'date', colour= etc)
            no_variable_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()} (UTC)', inline= False)
            no_variable_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
            no_variable_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
            no_variable_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
            no_variable_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
            no_variable_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
            no_variable_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
            
            await ch.send(embed = no_variable_embed)
            confirm = f"정상 실행 > {await print_time.get_UTC()} > date > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}" ; print(confirm)
         

async def setup(app):
    await app.add_cog(date(app))