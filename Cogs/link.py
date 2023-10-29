# 봇 서버 링크 안내 명령어
# Last Update : 231030

import discord
from discord.ext import commands
from discord import app_commands
from .utils import settings

log_channel = int(settings.log_channel)
        
class link(commands.Cog):
    def __init__(self,app : commands.Bot):
        self.app = app
        
    @app_commands.command(name="link",description="봇 서버 링크를 알 수 있습니다!")
    @app_commands.guild_only()
    async def link(self, interaction : discord.Interaction):
        await interaction.response.send_message("https://discord.gg/8dpAFYXk8s", ephemeral=False)     
        
        ch = self.app.get_channel(log_channel)
        confirm = f"정상 실행 > link > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}"
        
        print(confirm) ; await ch.send(confirm)
        
async def setup(app):
    await app.add_cog(link(app))