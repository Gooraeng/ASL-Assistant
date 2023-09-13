import discord
from discord.ext import commands
from discord import app_commands

        
class link(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="link",description="봇 서버 링크를 알 수 있습니다!")
    async def link(self, interaction : discord.Interaction):
        embed = discord.Embed(title="연락처",colour=0xffffff)
        embed.add_field(name="이메일", value="birdyoon1998@gmail.com")
        await interaction.response.send_message("https://discord.gg/bREZvQqFTT",ephemeral=False)
        
async def setup(app):
    await app.add_cog(link(app))