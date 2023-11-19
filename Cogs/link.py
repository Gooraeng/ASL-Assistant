# 봇 서버 링크 안내 명령어
# Last Update : 231115

import discord

from discord.ext import commands
from discord import app_commands
from .utils import settings, print_time
from .utils.embed_log import succeed, failed, etc

log_channel = int(settings.log_channel)
        
class link(commands.Cog):
    def __init__(self,app : commands.Bot):
        self.app = app
        
    @app_commands.command(name="link",description="봇 서버 링크를 알 수 있습니다!")
    async def link(self, interaction : discord.Interaction):
        await interaction.response.send_message("https://discord.gg/8dpAFYXk8s", ephemeral=False)     
        ch = self.app.get_channel(log_channel)        
        
        no_variable_embed = discord.Embed(title= '정상 실행', description= f'link', colour= etc)
        no_variable_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()} (UTC)', inline= False)
        no_variable_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
        no_variable_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
        no_variable_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
        no_variable_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
        no_variable_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
        no_variable_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
        
        await ch.send(embed = no_variable_embed)
        confirm = f"정상 실행 > {await print_time.get_UTC()} > link > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}" ; print(confirm)

        
       
    
    @link.error
    async def link_error_is_dm(self, interaction : discord.Interaction, error : app_commands.AppCommandError):
        ch = self.app.get_channel(log_channel) 
        
        if isinstance(error, app_commands.CommandInvokeError):
            
            no_variable_embed_dm = discord.Embed(title= '정상 실행', description= f'link', colour= etc)
            no_variable_embed_dm.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()} (UTC)', inline= False)
            no_variable_embed_dm.add_field(name='채널명 (ID)', value= f'DM ({interaction.channel.id})', inline= True)
            no_variable_embed_dm.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
            no_variable_embed_dm.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
            
            await ch.send(embed = no_variable_embed_dm)
            confirm = f"정상 실행 > {await print_time.get_UTC()} > link > 서버: - > 채널 : DM ({interaction.channel.id}) > 실행자: {interaction.user.display_name}" ; print(confirm)
    
                
async def setup(app):
    await app.add_cog(link(app))