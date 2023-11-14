# 메인 코드 모음
# Last update : 231113

import discord
import os
import Cogs.utils.settings as settings

from discord.ext import commands
from Cogs.utils import manage_tool as mt
from Cogs.utils import print_time as pt
from datetime import datetime as dt

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

app = commands.Bot(command_prefix="?",intents=intents)

discord_api_token = str(settings.discord_api_token)

car_img = settings.car_img
car_list = str(settings.car_list)
log_channel = int(settings.log_channel)

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
    print(f"{app.user.name} 준비 중")
    try:
        await load_extensions()
        await pt.get_UTC()
        print('---------------------------------------')
        await mt.print_CP()
        print('---------------------------------------')  
        
        synced = await app.tree.sync()
        print(f"명령어 {len(synced)}개 사용 가능")
        current_status = discord.Game(name='ASL에 정보제공')
        await app.change_presence(status=discord.Status.online,activity=current_status)
        print(f"{app.user.name}이(가) 준비되었습니다!")
        ch = app.get_channel(log_channel)
        await ch.send(f"## [{app.user.name} 작동 시작 // `{dt.utcnow()} (UTC)`]")
    
    except Exception as e:
        print(e)

@app.event
async def on_message(ctx : discord.Message) -> None:
    if ctx.author.bot or not app.is_ready():
        pass

@app.event
async def on_guild_join(guild):
    invite = discord.Invite
    ch = app.get_channel(log_channel)
    inviter_name = invite.inviter.name
    inviter_id = invite.inviter.id
    
    guild_joined_log = f'서버 입장 > 서버명 : {guild.name} (ID : {guild.id}) > 초대자 : {inviter_name} (ID : {inviter_id})'
    
    await ch.send(guild_joined_log)
    
    print('---------------------------------------') 
    print(guild_joined_log)
    print('---------------------------------------') 
    
       
# 에러 관리
@app.event
async def on_command_error(interaction : discord.Interaction, error):
    # 존재하지 않는 명령어 에러처리
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="오류",description="존재하지 않는 명령어입니다.",colour=0xFF0000)
        await interaction.response.send_message("",embed=embed,ephemeral=True, delete_after= 5) 

    # 명령어 오류 처리
    else:
        embed = discord.Embed(title="오류",description="예기치 못한 오류가 발생했습니다.",colour=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await interaction.response.send_message("",embed=embed,ephemeral=True)  

def main():
    app.run(discord_api_token)

# 메인 실행
if __name__ == '__main__':
    main()
