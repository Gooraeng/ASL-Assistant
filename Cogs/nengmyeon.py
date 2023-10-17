# ㅋㅋ
# Last update : 231017

import discord
from discord import app_commands
from discord.ext import commands

class nengmyeon(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    @app_commands.command(name='selju', description='ㅋㅋ')    
    async def show_nengmyeon_bab(self, interaction : discord.Interaction):
        embed = discord.Embed(title='ㅋㅋ', description='', colour=0xff0000)
        await interaction.response.send_message('',embed=embed,ephemeral=True,delete_after=5,file=discord.File('./images/nengmyeon.jpg'))        

async def setup(app):
    await app.add_cog(nengmyeon(app))