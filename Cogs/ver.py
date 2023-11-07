# 현재 봇의 마지막 업데이트 버전을 알려주는 명령어
# Last Update : 231107

import discord

from discord.ext import commands
from discord import app_commands
from .utils import settings, print_time

log_channel = int(settings.log_channel)
        
class ver(commands.Cog):
    def __init__(self,app : commands.Bot):
        self.app = app
        
    @app_commands.command(name="ver",description="현재 봇의 마지막 업데이트 날짜를 알려줍니다!")
    @app_commands.guild_only()
    async def ver(self, interaction : discord.Interaction):
        embed=discord.Embed(title="마지막 업데이트", description="2023/11/07", color=0x7fe6e4)
        embed.add_field(name='',value='정보가 없는 차량이 있을 수 있습니다. 하지만, 꼭 업데이트 될 겁니다!', inline=False)
        embed.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤 사라집니다!')
        await interaction.response.send_message("",embed=embed, ephemeral=True,delete_after=10)
        
        ch = self.app.get_channel(log_channel)
        
        confirm = f"정상 실행 > {await print_time.get_UTC()} > ver > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}"
        print(confirm) ; await ch.send(confirm)
        
async def setup(app):
    await app.add_cog(ver(app))