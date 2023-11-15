# 피드백 요청을 남기는 명령어
# Last Update : 231113

import discord
import asyncio

from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, View
from .utils import print_time, settings


feedback_log_channel = int(settings.feedback_log_channel)
log_channel = int(settings.log_channel)

# 명령어 함수 
class SpawnModal(commands.Cog):
    def __init__(self, app : commands.Bot) :
        self.app = app

        
    @app_commands.command(name= 'feedback', description= '뭔가 피드백을 남기고 싶은 게 있나요?')
    @app_commands.checks.cooldown(1, 30, key= lambda i :(i.guild_id, i.user.id))
    @app_commands.guild_only()
    async def warn_spawnmodal(self, interaction : discord.Interaction):
        log_ch = interaction.client.get_channel(log_channel)
        
        embed_warn = discord.Embed(title= '❗경고', description= '문제 전송 시 중간에 취소할 수 없습니다!', colour= 0xf50900)

        # await interaction.response.send_message('', embeds= embed_warn, view= warn_before(), ephemeral= True, delete_after= 60)
        
        confirm = f"정상 실행 > {await print_time.get_UTC()} > feedback > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name}"
        await log_ch.send(confirm); print(confirm)   
        
        
        # 베타 테스트 임베드 표시
        embed_beta_test = discord.Embed(title= '베타 테스트 기간', colour= 0xf50900,
                                        description= '2023년 11월 13일 오후 10시 ~ 2023년 11월 17일 0시')
        
        if interaction.channel.id == 1174018559685447760:
            embed_warn.add_field(name= '', value= '버튼 클릭마다 30초의 쿨타임이 존재합니다!', inline= False)
            embed_warn.add_field(name= '', value= '숙지하셨다면 어떤 문제를 신고하실 것인지 버튼을 눌러 진행해주십시오.', inline= False)
            
            await interaction.response.defer(ephemeral= True, thinking= True)
            await asyncio.sleep(0.5)
            await interaction.followup.send(embeds= [embed_beta_test, embed_warn], view= warn_before_asl_assistant_only())
           
        else:
            embed_warn.add_field(name= '', value= '이 명령어를 실행하실 때 마다 30초의 쿨타임이 존재합니다!', inline= False)
            embed_warn.add_field(name= '', value= '숙지하셨다면 어떤 문제를 신고하실 것인지 버튼을 눌러 진행해주십시오.', inline= False)
            embed_warn.add_field(name= '', value= '이 메세지는 60초 안에 지워집니다.')
            await interaction.response.send_message('', embeds= [embed_beta_test, embed_warn], view= warn_before(), ephemeral= True, delete_after= 60)
          
    @warn_spawnmodal.error
    async def cooldown_err(self, interaction : discord.Interaction, error : app_commands.AppCommandError):
        ch = self.app.get_channel(log_channel)
        if isinstance(error, app_commands.CommandOnCooldown):
            
            embed_cd_error = discord.Embed(title= '어이쿠! 아직 이용하실 수 없습니다!',
                                           description= f'{int(error.retry_after)}초 후에 다시 시도해주세요!',
                                           colour= 0xf40404)
            
            await interaction.response.send_message(embed= embed_cd_error, delete_after=5, ephemeral= True)
            
            err = f"오류 > {await print_time.get_UTC()} > feedback > 서버: {interaction.guild.name} > 채널 : {interaction.channel.name} > 실행자: {interaction.user.display_name} > timeout_err"
            await ch.send(err)
            
            print('---------------------------------------') 
            print(err)
            print('---------------------------------------') 
    
class FixModal(Modal, title = '데이터 수정 요청'):    
        
    fix_problem = discord.ui.TextInput(
        label= '세부 설명(필수)',
        style= discord.TextStyle.long,
        placeholder= '문제를 자세히 적어주세요!',
        max_length= 1000,
        required= True,
    )
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        
        feedback_ch = interaction.client.get_channel(feedback_log_channel)
        
        embed_sent = discord.Embed(title= '전송 완료', description= '정상적으로 전송이 완료되었습니다!', colour= 0x09f000)
        await interaction.response.send_message(embed= embed_sent, ephemeral= True, delete_after= 10)
        
        
        embed_problem = discord.Embed(title= 'Feedback 추가', description= '데이터 수정 요청', colour= 0x09f000)
        embed_problem.add_field(name= '서버명', value= f'{interaction.guild.name}', inline= True)
        embed_problem.add_field(name= '유저명 (Global)', value= f'{interaction.user.global_name}')
        embed_problem.add_field(name= '문제 묘사', value= self.fix_problem.value, inline= False)
        
        await feedback_ch.send(embed= embed_problem)
        
    
class SuggestModal(Modal, title= '기타 제안'):    
    
    suggest = discord.ui.TextInput(
        label= '세부 설명(필수)',
        style= discord.TextStyle.long,
        placeholder= '자세히 적어주세요!',
        max_length= 1000,
        required= True,
    )
    
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        
        feedback_ch = interaction.client.get_channel(feedback_log_channel)
        
        embed_sent = discord.Embed(title= '전송 완료', description= '정상적으로 전송이 완료되었습니다!', colour= 0x09f000)
        await interaction.response.send_message(embed= embed_sent, ephemeral= True, delete_after= 10)
        
        
        embed_problem = discord.Embed(title= 'Feedback 추가', description= '기타 제안', colour= 0x0407f9)
        embed_problem.add_field(name= '서버명', value= f'{interaction.guild.name}', inline= True)
        embed_problem.add_field(name= '유저명 (Global)', value= f'{interaction.user.global_name}')
        embed_problem.add_field(name= '문제 묘사', value= self.suggest.value, inline= False)
        
        await feedback_ch.send(embed= embed_problem)
        
             
        
class ReportModal(Modal, title = '봇 작동 신고'):    
            
    problem = discord.ui.TextInput(
        label= '세부 설명(필수)',
        style= discord.TextStyle.long,
        placeholder= '문제를 자세히 적어주세요!',
        max_length= 1000,
        required= True,
    )
    
    async def on_submit(self, interaction: discord.Interaction) -> None:
        feedback_ch = interaction.client.get_channel(feedback_log_channel)
        
        embed_sent = discord.Embed(title= '전송 완료', description= '정상적으로 전송이 완료되었습니다!', colour= 0x09f000)
        await interaction.response.send_message(embed= embed_sent, ephemeral= True, delete_after= 10)
        
        embed_problem = discord.Embed(title= '봇 작동 신고', description= 'Report', colour= 0xf50500)
        embed_problem.add_field(name= '서버명', value= f'{interaction.guild.name}', inline= True)
        embed_problem.add_field(name= '유저명 (Global)', value= f'{interaction.user.global_name}')
        embed_problem.add_field(name= '세부 설명', value= self.problem.value, inline= False)
        
        await feedback_ch.send(embed= embed_problem)
        
        
        
class warn_before(View):
    def __init__(self):
        super().__init__(timeout= None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.member)
        
    @discord.ui.button(label= '봇 작동 신고', style= discord.ButtonStyle.danger, custom_id= 'button_cooldown')
    async def report_prob(self, interaction : discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_modal(ReportModal())
        await interaction.delete_original_response()
          
        
    @discord.ui.button(label= '데이터 수정 요청', style= discord.ButtonStyle.green)
    async def request_fix(self, interaction : discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_modal(FixModal())
        await interaction.delete_original_response()
        
    
    @discord.ui.button(label= '기타 제안', style= discord.ButtonStyle.primary)
    async def suggestion(self, interaction : discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_modal(SuggestModal())
        await interaction.delete_original_response()

        
class warn_before_asl_assistant_only(View):
    def __init__(self):
        super().__init__(timeout= None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.member)
        
    @discord.ui.button(label= '봇 작동 신고', style= discord.ButtonStyle.danger, custom_id= 'button_cooldown_1')
    async def report_prob(self, interaction : discord.Interaction, button : discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        
        embed_cd_error = discord.Embed(title= '버튼을 마구 누르시면 안 됩니다!',
                                           description= f'{int(retry)}초 후에 다시 시도해주세요!',
                                           colour= 0xf40404)
        
        if retry:
            await interaction.response.send_message(embed= embed_cd_error, ephemeral= True, delete_after= 10)
        
        else:
            await interaction.response.send_modal(ReportModal())
        
          
        
    @discord.ui.button(label= '데이터 수정 요청', style= discord.ButtonStyle.green, custom_id= 'button_cooldown_2')
    async def request_fix(self, interaction : discord.Interaction, button : discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        
        embed_cd_error = discord.Embed(title= '버튼을 마구 누르시면 안 됩니다!',
                                           description= f'{int(retry)}초 후에 다시 시도해주세요!',
                                           colour= 0xf40404)
        
        if retry:
            await interaction.response.send_message(embed= embed_cd_error, ephemeral= True, delete_after= 10)
        
        else:
            await interaction.response.send_modal(FixModal())
        
        
    
    @discord.ui.button(label= '기타 제안', style= discord.ButtonStyle.primary, custom_id= 'button_cooldown_3')
    async def suggestion(self, interaction : discord.Interaction, button : discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        
        embed_cd_error = discord.Embed(title= '버튼을 마구 누르시면 안 됩니다!',
                                           description= f'{int(retry)}초 후에 다시 시도해주세요!',
                                           colour= 0xf40404)
        
        if retry:
            await interaction.response.send_message(embed= embed_cd_error, ephemeral= True, delete_after= 10)
        
        else:
            await interaction.response.send_modal(SuggestModal()) 
 
              
async def setup(app : commands.Bot):
    await app.add_cog(SpawnModal(app))