import discord
from discord.ext import commands
from discord import app_commands

class buttonfunction(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(discord.ui.Button(label="구랭 유튜브",url="http://www.youtube.com/@gooraeng"))
        
class qna(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="qna",description="봇 제작자의 연락처를 알려줍니다!")
    async def qna(self, interaction : discord.Interaction):
        embed = discord.Embed(title="연락처",colour=0xffffff)
        embed.add_field(name="1. 이메일", value="birdyoon1998@gmail.com")
        await interaction.response.send_message("",embed=embed,view=buttonfunction(),ephemeral=True)
        
async def setup(app):
    await app.add_cog(qna(app))