from keep_alive import keep_alive
import discord, asyncio, datetime, json, config, os
from discord.ext import commands
from discord.ext.commands import has_permissions
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, Option, OptionType
from pymongo import pymongo

bot = commands.Bot(
  command_prefix="$",
  case_insensitive=False,
  intents=discord.Intents.all(),
  help_command=None
)



slash = InteractionClient(bot)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.channel.id == 962359313987416094:
    await message.delete()
    check = bot.get_channel(962351443162067075)
    status = bot.get_channel(962342213398970450)
    post = bot.get_channel(962359313987416094)
    m=await message.channel.send(f'**Hi , {message.author.name}  Your Job Post is sent for verification. Keep checking {status.mention} for verification updates **')
    await asyncio.sleep(3)
    await m.delete()
    text = f'{message.author.name}#{message.author.discriminator}'
    await check.send(f'**USER NAME - ** `{text}`')
    await check.send(f"**🔴 ATTENTION 🔴** \n {message.author.mention} Uploaded a new job post\n {message.content} " ,
      components=[
        ActionRow(
          Button(
            style=ButtonStyle.green,
            label="APPROVE POST",
            custom_id='yes',
          ),
          Button(
            style=ButtonStyle.red,
            label="DISAPPROVE POST",
            custom_id='no',
          ),
          Button(
            style=ButtonStyle.green,
            label=f"{message.author.id}",
            custom_id='statusgood',
          ),
          Button(
            style=ButtonStyle.red,
            label=f"{message.author.id}",
            custom_id='statusbad',
          )
        )
    ])            
    
    await check.send('============================================================')
    await status.send(f'**STATUS REPORT FOR {message.author.mention}**')
    embed=discord.Embed(title='REPORT :-', description ='Status of your job post - **Under Verification**', color=discord.Color.blurple())
    await status.send(embed=embed)
    await status.send('============================================================')
    



    

@bot.event 
async def on_button_click(interaction):
  if interaction.component.custom_id == 'yes':
    post = bot.get_channel(962359313987416094)
    status = bot.get_channel(962342213398970450)
    if not interaction.author.guild_permissions.manage_messages:
      await interaction.respond(":x: You are missing `manage_messages` permission", ephemeral=True)
      raise Exception()
    await interaction.message.edit(components=[
        ActionRow(
          Button(
            style=ButtonStyle.green,
            label=f"THE ABOVE POST IS APPROVED BY {interaction.author}",
            disabled=True
          )
        )
    ])
    await post.send(interaction.message.content)
    await post.send('============================================================')
    await interaction.respond()
    
  if interaction.component.custom_id == 'no':
    status = bot.get_channel(962342213398970450)
    if interaction.component.custom_id == "no":
      if not interaction.author.guild_permissions.manage_messages:
        await interaction.respond(":x: You are missing `manage_messages` permission", ephemeral=True)
        raise Exception()
    await interaction.message.edit(components=[
        ActionRow(
          Button(
            style=ButtonStyle.red,
            label=f"THE ABOVE POST IS DISAPPROVED BY {interaction.author}",
            disabled=True
          )
        )
    ])
    await interaction.respond()

  if interaction.component.custom_id == 'statusgood':
    user_id = interaction.component.label
    status = bot.get_channel(962342213398970450)
    post = bot.get_channel(962359313987416094)
    await status.send(f'**STATUS REPORT FOR <@{user_id}>**')
    embed=discord.Embed(title='REPORT :-', description =f'Status of your job post - **✅ Verification Passed ** `posted in `{post.mention}', color=discord.Color.green())
    await status.send(embed=embed)
    await status.send('============================================================')
    await interaction.respond()

  if interaction.component.custom_id == 'statusbad':
    user_id = interaction.component.label
    status = bot.get_channel(962342213398970450)
    await status.send(f'**STATUS REPORT FOR <@{user_id}>**')
    embed=discord.Embed(title='REPORT :-', description ='Status of your job post - ** Verification Failed ** `Contact staff team for further details `', color=discord.Color.red())
    await status.send(embed=embed)
    await status.send('============================================================')
    await interaction.respond()
      
    

  
    


@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="to anything"))
  print(f"Logged in as {bot.user.name}")



keep_alive()

bot.run(os.environ['BOT KEY'])
    
    
    
    