from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
import os

class spec(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="spec",description="차량의 성능을 확인합니다")
    @app_commands.describe(cars_name="차량 성능 확인")
    async def cars__name(self, interaction : discord.Interaction, cars_name: str):
        await interaction.response.send_message(f"차량 : {cars_name}")


async def setup(app):
    await app.add_cog(spec(app))            