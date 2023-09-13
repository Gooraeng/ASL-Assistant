
import discord
from discord.ext import commands
from discord import app_commands

car=[["ginetta g60","https://cdn.discordapp.com/attachments/847171495812661248/995649108339609600/ginetta.png"],
     ["bmw z4","https://media.discordapp.net/attachments/847170453374369893/995644046032769064/z4.png"]
    ]

class spec(commands.Cog):
    def __init__(self,app):
        self.app = app
        
    @app_commands.command(name="spec",description="차량의 성능을 확인합니다")
    @app_commands.describe(cars_name="차량 성능 확인")
    async def spectation(interaction: discord.Interaction,
                         car_name: typing.Literal):
        return
    
    @spectation.autocomplete("car_name")
    async def spectation_autocompletion(
        interaciton: discord.Interaction,
        current: str
    ) 
    
async def setup(app):
    await app.add_cog(spec(app))



