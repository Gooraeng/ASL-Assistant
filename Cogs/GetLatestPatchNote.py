# 최신 패치노트 출력하는 명령어
# Last Update : 231216

from discord import Interaction, app_commands
from discord.ext import commands
from .utils import settings
from .utils.not_here import not_here_return_embed
from .utils.renew_patchnote import get_patchnote_link, get_patchnote_title

log_channel = int(settings.log_channel)
feedback_log_channel = int(settings.feedback_log_channel)


class GetPatchNote(commands.Cog):
    def __init__(self, app : commands.Bot) -> None:
        self.app = app
        
    
    @app_commands.command(name= '패치노트', description= '가장 최신의 패치 노트를 알려줍니다')
    async def send_patchnote(self, interaction : Interaction):
        
        if interaction.channel.id == log_channel or interaction.channel.id == feedback_log_channel:
            return await not_here_return_embed(interaction= interaction) 
        
        await interaction.response.send_message(content= f'# 패치노트명 : {await get_patchnote_title()}\n{await get_patchnote_link()}', ephemeral= True)
    
    @send_patchnote.error
    async def srl_error(self, interaction : Interaction, error : app_commands.AppCommandError):
        
        if isinstance(error, app_commands.CommandInvokeError):
            pass
    


async def setup(app : commands.Bot):
    await app.add_cog(GetPatchNote(app))