# embed 컬러관리
# Last Update : 231115
succeed = 0x79e85e
failed = 0xfe7866
etc = 0x97c8f6


    
# async def no_variable(interaction : Interaction):
#     no_variable_embed = discord.Embed(title= '정상 실행', description= f'{app_commands.command.__name__}')
    
#     no_variable_embed.add_field(name='시간(UTC)', value= get_UTC())
    
#     no_variable_embed.add_field(name='서버명', value= f'{interaction.guild.name}', inline= True)
#     no_variable_embed.add_field(name='서버 ID', value= f'{interaction.guild.id}', inline= False)
    
#     no_variable_embed.add_field(name='채널명', value= f'{interaction.channel.name}', inline= True)
#     no_variable_embed.add_field(name='채널 ID', value= f'{interaction.channel.id}', inline= False)
    
#     no_variable_embed.add_field(name='유저', value= f'{interaction.user.display_name}', inline= True)
#     no_variable_embed.add_field(name='유저 ID', value= f'{interaction.user.id}', inline= False)
    
    
#     return await ch.send(embed= no_variable_embed)