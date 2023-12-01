# 후원 링크 전송 명령어
# Last Update : 231125

import discord

from discord.ext import commands
from discord import app_commands
from .utils import settings, print_time
from .utils.not_here import not_here_return_embed
from .utils.embed_log import succeed, failed, etc


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)
      
class Donation(commands.Cog):
    def __init__(self,app : commands.Bot):
        self.app = app
    
  
    @app_commands.command(name="donate", description="봇 개발자에게 따뜻한 캔 커피 하나 값을 후원해주실 수 있으실까요?")
    async def donate(self, interaction : discord.Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
          
        ch = self.app.get_channel(log_channel)        

        await interaction.response.send_message("## 이용해주셔서 매번 감사드립니다!\n\nhttps://twip.kr/gooraeng_", ephemeral= True)   
            
        no_variable_embed = discord.Embed(title= '정상 실행', description= f'donate', colour= etc)
        no_variable_embed.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
        no_variable_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
        no_variable_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
        no_variable_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
        no_variable_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
        no_variable_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
        no_variable_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
        
        await ch.send(embed = no_variable_embed)
        confirm = f"정상 실행 > {await print_time.get_UTC()} > donate > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}" ; print(confirm)

            
    @donate.error
    async def donate_error(self, interaction : discord.Interaction, error : app_commands.AppCommandError):
        ch = self.app.get_channel(log_channel)
        
        if isinstance(error, app_commands.CommandInvokeError):
            if interaction.channel.type == discord.ChannelType.private:
                no_variable_embed_dm = discord.Embed(title= '정상 실행', description= f'donate', colour= etc)
                no_variable_embed_dm.add_field(name='시간(UTC)', value= f'{await print_time.get_UTC()}', inline= False)
                no_variable_embed_dm.add_field(name='채널명 (ID)', value= f'DM ({interaction.channel.id})', inline= True)
                no_variable_embed_dm.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
                no_variable_embed_dm.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
                    
                await ch.send(embed = no_variable_embed_dm)
                confirm = f"정상 실행 > {await print_time.get_UTC()} > donate > 서버: - > 채널 : DM ({interaction.channel.id}) > 실행자: {interaction.user.display_name}" ; print(confirm)
            else:
                pass


              
async def setup(app : commands.Bot):
    await app.add_cog(Donation(app))