# 현재 봇의 날짜 버전을 알려주는 명령어

import discord
from discord.ext import commands
from discord import app_commands

        
class ver(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="ver",description="현재 봇의 마지막 업데이트 날짜를 알려줍니다!")
    async def ver(self, interaction : discord.Interaction):
        embed=discord.Embed(title="마지막 업데이트", description="2023/10/07", color=0x7fe6e4)
        embed.add_field(name='',value='정보가 없는 차량이 있을 수 있습니다. 하지만, 꼭 업데이트 될 겁니다!', inline=False)
        embed.add_field(name='',value='**<경고>** 이 메세지는 10초 뒤 사라집니다!')
        await interaction.response.send_message("",embed=embed, ephemeral=True,delete_after=10)
        
async def setup(app):
    await app.add_cog(ver(app))