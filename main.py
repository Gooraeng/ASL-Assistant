# 메인 코드 모음
# Last update : 231123

import discord
import os
import Cogs.utils.settings as settings

from discord.ext import commands
from Cogs.utils import manage_tool as mt
from Cogs.utils import print_time as pt
from Cogs.utils.embed_log import succeed, failed, etc, interaction_with_server


intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

app = commands.Bot(command_prefix="!!",intents=intents)
discord_api_token = str(settings.discord_api_token)

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


# ASL ASSISTANT load extention
@app.event
async def setup_hook():
    print(f"{app.user.name} 준비 중")
    
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
    
    await pt.get_UTC()
    print('---------------------------------------')
    await mt.print_CP()
    print('---------------------------------------') 
    
    synced = await app.tree.sync()
    print(f"명령어 {len(synced)}개 사용 가능")             
                  

# ASL ASSISTANT 준비 완료 상태
@app.event
async def on_ready():
    ch = app.get_channel(log_channel)
   
    current_status = discord.Game(name= 'ASL에 정보제공')
    await app.change_presence(status= discord.Status.online, activity= current_status)
    
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


# 메세지 전송 이벤트 처리    
@app.event
async def on_message(ctx : discord.Message) -> None:
    if ctx.author.bot == True:
        pass
    
    else:
        if ctx.channel.id == log_channel or ctx.channel.id == feedback_log_channel:
            not_here_embed = discord.Embed(title= '여기는 로그가 남는 채널입니다', description= f'5초 후에 지워집니다.', colour= 0xfe7866)
            await ctx.delete()
            await ctx.channel.send(embed= not_here_embed, delete_after= 5, mention_author= True)


# 서버 입장 이벤트 
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


# 서버 퇴장 이벤트
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
    # 존재하지 않는 명령어
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
async def on_error(error : Exception):    
    if isinstance(error, discord.ConnectionClosed):
        print(error); return await app.connect(reconnect= True)
    
    if isinstance(error, discord.DiscordServerError):
        print(error); return await app.connect(reconnect= True)
    
    if isinstance(error, discord.GatewayNotFound):
        print(error); return await app.connect(reconnect= True)
    
    else: raise error
    
         
def main():
    app.run(discord_api_token)


# 메인 실행
if __name__ == '__main__':
    main()