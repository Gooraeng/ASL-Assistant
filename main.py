# 메인 코드 모음

import discord
import os
from discord.ext import commands

import settings
import config


intents = discord.Intents.default()
intents.message_content = True
app = commands.Bot(command_prefix="?",intents=intents,)
discord_api_token = str(settings.discord_api_token)

    
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
            except commands.ExtensionAlreadyLoaded:
                print(f"{filename[:-3]} 이 이미 로드되었습니다.")
       
# 봇 이벤트
@app.event
async def on_ready():
    print(f"{app.user.name} 준비 중")
    try:
        await load_extensions()
        print('---------------------------------------')
        await config.check_update()
        print('---------------------------------------')  
        
        synced = await app.tree.sync()
        print(f"명령어 {len(synced)}개 사용 가능")
        current_status = discord.Game(name='ASL에 정보제공')
        await app.change_presence(status=discord.Status.online,activity=current_status)
        print(f"{app.user.name}이(가) 준비되었습니다!")
                    
    except Exception as e:
        print(e)
        
async def on_message(self, message : discord.Message) -> None:
    if message.author.bot:
        return

async def on_guild_join(self, guild : discord.Guild) -> None:
    if guild.id in self.blacklist:
        await guild.leave()
    

            
# 에러 관리
async def on_command_error(ctx, interaction : discord.Interaction, error):
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