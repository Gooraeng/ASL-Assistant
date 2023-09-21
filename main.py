# 메인 관련 메소드 임포트
import asyncio
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import settings
import car_list


intents = discord.Intents.default()
app = commands.Bot(command_prefix="/",intents=intents)

# 확장 기능(명령어) 로드
async def load_extensions():
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            try:
                await app.load_extension(f"Cogs.{filename[:-3]}")            
# 오류 처리
            except (commands.NoEntryPointError, commands.ExtensionFailed):
                print(f"파일 오류 발생 : {filename}")
            except commands.ExtensionNotFound:
                print(f"{filename[:-3]} 파일이 존재하지 않습니다.")
       

# 봇 이벤트
@app.event
async def on_ready():   
    print(f"{app.user.name} 준비 중")
    try:
        synced = await app.tree.sync()
        print(f"명령어 {len(synced)}개 사용 가능")
        current_status = discord.Game(name='A9차량 정보제공')
        await app.change_presence(status=discord.Status.online,activity=current_status)
        print(f"{app.user.name}이(가) 준비되었습니다!")
        while True:           
            await asyncio.sleep(86400)
            print('---------------------------------------')
            await car_list.Managing.make_a9_car_list()
            await car_list.Managing.check_uptate()
            print('갱신 완료')
            
    except Exception as e:
        print(e)
async def on_command_error(ctx, interaction : discord.Interaction, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="오류",description="존재하지 않는 명령어입니다.",colour=0xFF0000)
        await interaction.response.send_message("",embed=embed,ephemeral=True) 
    else:
        embed = discord.Embed(title="오류",description="예기치 못한 오류가 발생했습니다.",colour=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await interaction.response.send_message("",embed=embed,ephemeral=True)
    

# 메인
async def main():
    async with app:
        await load_extensions()
        await car_list.Managing.make_a9_car_list()
        print('---------------------------------------')
        await car_list.Managing.check_uptate()
        print('---------------------------------------')
        await app.start(settings.token)
        
# 메인 실행
asyncio.run(main())