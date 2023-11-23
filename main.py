# 메인 코드 모음
# Last update : 231123

import discord
import os
import Cogs.utils.settings as settings

from discord import app_commands
from discord.ext import commands
from Cogs.utils import manage_tool as mt
from Cogs.utils import print_time as pt
from Cogs.utils.embed_log import succeed, failed, etc, interaction_with_server
from typing import Literal

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

app = commands.Bot(command_prefix="!!",intents=intents)
discord_api_token = str(settings.discord_api_token)

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)

# 확장 기능(명령어) 로드
async def load_extensions():
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            try:
                await app.load_extension(f"Cogs.{filename[:-3]}")            
# 오류 처리
            except (commands.NoEntryPointError, commands.ExtensionFailed) as e:
                print(f"파일 오류 발생 : {filename}")
                print(e)
            except commands.ExtensionNotFound:
                print(f"{filename[:-3]} 파일이 존재하지 않습니다.")
            except commands.ExtensionAlreadyLoaded:
                print(f"{filename[:-3]} 이(가) 이미 로드되었습니다.")
       
# 봇 이벤트
@app.event
async def on_ready():
    
    ch = app.get_channel(log_channel)
    
    print(f"{app.user.name} 준비 중")
    
    await load_extensions()
    synced = await app.tree.sync()
    print(f"명령어 {len(synced)}개 사용 가능")   
    
    current_status = discord.Game(name= 'ASL에 정보제공')
    await app.change_presence(status= discord.Status.online, activity= current_status)
    await pt.get_UTC()
    print('---------------------------------------')
    await mt.print_CP()
    print('---------------------------------------') 
    print(f"{app.user.name}이(가) 준비되었습니다!")
    
    try:        
        if app.is_ready() :   
            ready_embed = discord.Embed(title= f'{app.user.name} 작동 시작' , description= f'{await pt.get_UTC()} (UTC)', colour= succeed)
            await ch.send(embed= ready_embed)
        
    except Exception as e:
        if not app.is_ready():
            not_ready_embed = discord.Embed(title= f'{app.user.name} 작동 실패' , description= f'{await pt.get_UTC()} (UTC)', colour= failed)
            not_ready_embed.add_field(name='사유', value= e)
            await ch.send(embed= not_ready_embed)
            
            print(e)

   
        
@app.event
async def on_message(ctx : discord.Message) -> None:
    
    if ctx.author.bot == True:
        pass
    
    else:
        if ctx.channel.id == log_channel or ctx.channel.id == feedback_log_channel:
            await ctx.delete()
            await ctx.channel.send('여기에서는 메세지를 보내실 수 없습니다!', delete_after= 3, mention_author= True)

            
@app.event
async def on_guild_join(guild):
    
    ch = app.get_channel(log_channel)    
    guild_joined_embed = discord.Embed(title= '서버 입장', description= f'{await pt.get_UTC()} (UTC)', colour= interaction_with_server)
    guild_joined_embed.add_field(name= '서버명', value= guild.name, inline= True)
    guild_joined_embed.add_field(name= '서버 ID', value= guild.id)
    
    await ch.send(embed= guild_joined_embed)
    
    print('---------------------------------------') 
    guild_joined_log = f'서버 입장 > {await pt.get_UTC()} > 서버명 : {guild.name} (ID : {guild.id})'
    print(guild_joined_log)
    print('---------------------------------------')


@app.event
async def on_guild_remove(guild):    
    ch = app.get_channel(log_channel)    
    
    guild_left_embed = discord.Embed(title= '서버 퇴장', description= f'{await pt.get_UTC()} (UTC)', colour= interaction_with_server)
    guild_left_embed.add_field(name= '서버명', value= guild.name, inline= True)
    guild_left_embed.add_field(name= '서버 ID', value= guild.id)
    
    await ch.send(embed= guild_left_embed)
    
    print('---------------------------------------') 
    guild_left_log = f'서버 퇴장 > {await pt.get_UTC()} > 서버명 : {guild.name} (ID : {guild.id})'
    print(guild_left_log)
    print('---------------------------------------')  


# 커맨드 에러 관리
@app.event
async def on_command_error(interaction : discord.Interaction, error):
    # 존재하지 않는 명령어 에러처리
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="오류",description="존재하지 않는 명령어입니다.",colour= failed)
        await interaction.response.send_message("", embed=embed, ephemeral=True, delete_after= 5) 

    # 명령어 오류 처리
    else:
        embed = discord.Embed(title="오류", description="예기치 못한 오류가 발생했습니다.", colour= failed)
        embed.add_field(name="상세", value=f"```{error}```")
        await interaction.response.send_message("",embed=embed,ephemeral=True)  


# 연결 에러 처리
@app.event
async def on_error(interaciton : discord.Interaction, error : Exception):
    
    ch = app.get_channel(log_channel)
    bot_developer = app.get_user(303915314062557185)
    
    if isinstance(error, discord.ConnectionClosed):
        error_embed1 = discord.Embed(title= '에러 발생', description= f'{pt.get_UTC()}', colour= failed)
        error_embed1.add_field(name= '사유', value= f'discord.ConnectionClosed / Koyeb 확인 요망')
        
        await ch.send(content= f'{bot_developer.mention}', embed= error_embed1); return await app.connect(reconnect= True)
    
    if isinstance(error, discord.DiscordServerError):
        error_embed2 = discord.Embed(title= '에러 발생', description= f'{pt.get_UTC()}', colour= failed)
        error_embed2.add_field(name= '사유', value= f'discord.DiscordServerError / 재연결 시도')
        
        await ch.send(embed= error_embed2); return await app.connect(reconnect= True)
    
    if isinstance(error, discord.GatewayNotFound):
        error_embed3 = discord.Embed(title= '에러 발생', description= f'{pt.get_UTC()}', colour= failed)
        error_embed3.add_field(name= '사유', value= f'discord.GatewayNotFound 에러')
        await ch.send(embed= error_embed3); return await app.connect(reconnect= True)
    
    else: raise error
    
    
         
def main():
    app.run(discord_api_token)

# 메인 실행
if __name__ == '__main__':
    main()