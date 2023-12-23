# 최신 패치노트 출력하는 명령어
# Last Update : 231223
import discord
import asyncio

from discord import Interaction, app_commands, Embed 
from discord.ext import commands
from .utils import settings
from .utils.embed_log import failed, etc
from .utils.not_here import not_here_return_embed
from .utils.renew_patchnote import get_patchnote_embed
from .utils.print_time import get_UTC


log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class buttonfuc(discord.ui.View):
    def __init__(self):
        super().__init__(timeout= None)
        self.add_item(discord.ui.Button(label= '패치노트 보기!', url= 'https://asphaltlegends.com/news'))
    
    
class GetPatchNote(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
        
    
    @app_commands.command(name= '최신패치노트', description= '가장 최신의 패치 노트를 알려줍니다')
    @app_commands.checks.cooldown(1, 600, key= lambda i :(i.guild_id, i.user.id))
    @app_commands.guild_only()
    async def send_patchnote(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
        
        title = await get_patchnote_embed()
        time = await get_UTC()
        
        if title == None:
            error_embed = Embed(title= '오류', description= '조회할 수 없습니다. 다시 시도해주세요!', colour= failed)
            await interaction.response.send_message(embed= error_embed, ephemeral= True, delete_after= 10)
            
            ch = self.app.get_channel(log_channel)
            not_loaded = f"오류 > {time} > 최신패치노트 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 패치 노트 조회 실패"
           
            log_embed_error = Embed(title= '오류', description= f'최신패치노트', colour= failed)
            log_embed_error.add_field(name='시간(UTC)', value= time, inline= False)
            log_embed_error.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
            log_embed_error.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
            log_embed_error.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
            log_embed_error.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
            log_embed_error.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
            log_embed_error.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
            log_embed_error.add_field(name='예기치 않은 오류' , value= '패치노트 출력 실패', inline= False)
            
            await ch.send(embed= log_embed_error)
            print(not_loaded)       
            
            
        
        else:
            try:
                await interaction.response.send_message(embed= title, view= buttonfuc())
            
            except Exception:
                await interaction.response.defer(thinking= True)
                asyncio.sleep(5000)
                await interaction.response.send_message(embed= title, view= buttonfuc())
            
    
    @send_patchnote.error
    async def srl_error(self, interaction : Interaction, error : app_commands.AppCommandError):
        title = await get_patchnote_embed()
        ch = self.app.get_channel(log_channel)
        time = await get_UTC()
        
        if isinstance(error, app_commands.CommandInvokeError):
            if title == None:
                error_embed_dm = Embed(title= '에러', description= f'최신패치노트', colour= etc)
                error_embed_dm.add_field(name='시간(UTC)', value= time, inline= False)
                error_embed_dm.add_field(name='채널명 (ID)', value= f'DM ({interaction.channel.id})', inline= True)
                error_embed_dm.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
                error_embed_dm.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
                error_embed_dm.add_field(name='예기치 않은 오류' , value= '패치노트 출력 실패', inline= False)                    
                
                await ch.send(embed = error_embed_dm)
                not_sent = f"에러 > {time} > 최신패치노트 > 서버: - > 채널 : DM ({interaction.channel.id}) > 실행자: {interaction.user.display_name}" ; print(not_sent)
            
            else:
                pass
        
        if isinstance(error, app_commands.CommandOnCooldown):
            embed_cd_error = discord.Embed(title= '어이쿠! 아직 이용하실 수 없습니다!',
                                           description= f'{int(error.retry_after // 60)}분 {int(error.retry_after % 60)}초 후에 다시 시도해주세요!',
                                           colour= failed)
            await interaction.response.send_message(embed= embed_cd_error, delete_after=5, ephemeral= True)
            
            no_variable_embed = discord.Embed(title= '에러', description= f'최신패치노트', colour= failed)
            no_variable_embed.add_field(name='시간(UTC)', value= time, inline= False)
            no_variable_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
            no_variable_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
            no_variable_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
            no_variable_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= True)
            no_variable_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= True)
            no_variable_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= True)
            no_variable_embed.add_field(name='사유', value= '타임 아웃', inline= False)
            await ch.send(embed = no_variable_embed)
            
            err = f"오류 > {time} > 최신패치노트 > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > 타임아웃 에러"
            print('---------------------------------------') 
            print(err)
            print('---------------------------------------') 
            
    


async def setup(app : commands.Bot):
    await app.add_cog(GetPatchNote(app))