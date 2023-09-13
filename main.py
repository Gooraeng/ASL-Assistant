import asyncio
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

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
                if filename == "car_spec.py":
                    print(f"car_spec.py 고장 - alternative 실행")
                    for filename in os.listdir("Cogs_alternative"):
                        if filename.endswith(".py"):
                            await app.load_extension(f"Cogs_alternative.{filename[:-3]}")
            except commands.ExtensionNotFound:
                print(f"{filename[:-3]} 파일이 존재하지 않습니다.")
            

# 이벤트
@app.event
async def on_ready():
    print(f"{app.user.name}이(가) 준비되었습니다!")
    try:
        synced = await app.tree.sync()
        print(f"명령어 {len(synced)}개 사용 가능")
        current_status = discord.Game(name='A9차량 정보제공')
        await app.change_presence(status=discord.Status.online,activity=current_status)
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
        load_dotenv()
        os.getenv
        tokens = os.getenv('token')
        await app.start(tokens)

# 메인 실행  
asyncio.run(main())