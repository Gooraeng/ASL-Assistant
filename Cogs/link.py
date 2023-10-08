# 봇 서버 링크 안내 명령어

import discord
from discord.ext import commands
from discord import app_commands

        
class link(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="link",description="봇 서버 링크를 알 수 있습니다!")
    async def link(self, interaction : discord.Interaction):
        await interaction.response.send_message("https://discord.gg/8dpAFYXk8s", ephemeral=False)     
       
async def setup(app):
    await app.add_cog(link(app))