# ㅋㅋ
# Last Update : 231030

import discord
from discord import app_commands
from discord.ext import commands
from .utils import settings, print_time

log_channel = int(settings.log_channel)

class nengmyeon(commands.Cog):
    def __init__(self, app: commands.Bot):
        self.app = app
    
    @app_commands.command(name='selju', description='ㅋㅋ')
    @app_commands.guild_only() 
    async def show_nengmyeon_bab(self, interaction : discord.Interaction):
        embed = discord.Embed(title='ㅋㅋ', description='', colour=0xff0000)
        await interaction.response.send_message('',embed=embed,ephemeral=True,delete_after=5,file=discord.File('./images/nengmyeon.jpg'))        
        
        ch = self.app.get_channel(log_channel)
        
        confirm = f"정상 실행 > {await print_time.get_UTC()} > selju > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}"
        print(confirm) ; await ch.send(confirm)
        
async def setup(app):
    await app.add_cog(nengmyeon(app))