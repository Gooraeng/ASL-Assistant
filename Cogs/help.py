# 사용 가능한 명령어들의 설명을 알려줌

import discord
from discord.ext import commands
from discord import app_commands

        
class help(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="help",description="사용할 수 있는 명령어를 정리했습니다!")
    async def qna(self, interaction : discord.Interaction):
        embed=discord.Embed(title="Help", description="사용할 수 있는 명령어를 정리했습니다!", color=0x7fe6e4)
        embed.add_field(name="---------------", value="", inline=True)
        embed.add_field(name="1. Spec", value="차량의 성능을 확인합니다! 이 기능은 외부 데이터에 의해 작동되므로 언제든지 비활성화 될 수 있습니다.", inline=False)
        embed.add_field(name="2. Ref", value="봇 제작에 있어 참고/활용된 자료의 출처를 알려줍니다!", inline=False)
        embed.add_field(name="3. Link", value="봇 서버 링크를 알 수 있습니다!", inline=False)
        embed.add_field(name="4. Qna", value="봇 제작자에게 직접 문의하실 수 있습니다!", inline=False)
        embed.add_field(name="5. Ver", value="현재 봇의 마지막 업데이트 날짜를 알려줍니다!", inline=False)
        
        await interaction.response.send_message("",embed=embed, ephemeral=True)
        
async def setup(app):
    await app.add_cog(help(app))