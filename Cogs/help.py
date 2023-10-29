# 사용 가능한 명령어들의 설명을 알려줌
# Last Update : 231030

import discord
from discord.ext import commands
from discord import app_commands
from .utils import settings, print_time

log_channel = int(settings.log_channel)
        
class help(commands.Cog):
    def __init__(self,app : commands.Bot):
        self.app = app
        
    @app_commands.command(name="help",description="사용할 수 있는 명령어를 정리했습니다!")
    @app_commands.guild_only()
    async def qna(self, interaction : discord.Interaction):
        embed=discord.Embed(title="Help", description="사용할 수 있는 명령어를 정리했습니다!", color=0x7fe6e4)
        embed.add_field(name="---------------", value="", inline=True)
        embed.add_field(name="1. Spec", value="차량의 성능을 확인합니다! 이 기능은 외부 데이터에 의해 작동되므로 언제든지 비활성화 될 수 있습니다.", inline=False)
        embed.add_field(name="2. Clash", value="클럽 클래시 레퍼런스를 보여줍니다!", inline=False)
        embed.add_field(name="3. Ref", value="봇 제작에 있어 참고/활용된 자료의 출처를 알려줍니다!", inline=False)
        embed.add_field(name="4. Link", value="봇 서버 링크를 알 수 있습니다!", inline=False)
        embed.add_field(name="5. Ver", value="현재 봇의 마지막 업데이트 날짜를 알려줍니다!", inline=False)
        embed.add_field(name="6. Selju", value="별다른 설명이 필요없습니다. 바로 시도해보세요!", inline=False)        
        embed.add_field(name="7. Date", value="향후 일정을 확인하실 수 있습니다!", inline=False)
        await interaction.response.send_message("",embed=embed, ephemeral=True)
        
        ch = self.app.get_channel(log_channel)
        confirm = f"정상 실행 > {await print_time.get_UTC()} > help > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}"
        
        print(confirm) ; await ch.send(confirm)
        
async def setup(app):
    await app.add_cog(help(app))