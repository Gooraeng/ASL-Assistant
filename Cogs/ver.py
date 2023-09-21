import discord
from discord.ext import commands
from discord import app_commands

        
class ver(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="ver",description="현재 봇의 마지막 업데이트 날짜를 알려줍니다!")
    async def ver(self, interaction : discord.Interaction):
        embed=discord.Embed(title="마지막 업데이트", description="2023/09/21", color=0x7fe6e4)
        await interaction.response.send_message("",embed=embed, ephemeral=True,delete_after=5)
        
async def setup(app):
    await app.add_cog(ver(app))