# car_spec.py 내 spec 명령어를 필요하는데 있어 레퍼런스가 된 자료들의 링크를 알려줌

import discord
from discord.ext import commands
from discord import app_commands


class ref(commands.Cog):
    def __init__(self, app):
        self.app = app
    
    @app_commands.command(name='ref', description='봇의 레퍼런스 및 출처를 알려줍니다.')
    async def ref(self, interaction : discord.Interaction):
        embed1=discord.Embed(title="레퍼런스 1 - MEI", url="https://www.mei-a9.info/", description='클릭 시 링크로 이동합니다.',color=0x7fe6e4)
        embed1.add_field(name="- 사용목적", value="아스팔트 9 차량 리스트 추출")
        
        embed2=discord.Embed(title="레퍼런스 2 - A9 Database", description='클릭 시 링크로 이동합니다.', url=" https://discord.gg/dVA7R9CXpB ", color=0x7fe6e4)
        embed2.add_field(name="- 사용목적", value="아스팔트 9 차량 데이터 베이스 활용")
        
        await interaction.response.send_message('',embeds=[embed1,embed2],ephemeral=True)

async def setup(app):
    await app.add_cog(ref(app))