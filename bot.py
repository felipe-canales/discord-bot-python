import os

import discord
from dotenv import load_dotenv

import commands as com
from config import load_p_users

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
cfg = Config()

client = discord.Client()


@client.event
async def on_ready():
    global p_users
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.content[0:3].lower() != "trz":
        return
    
    command = message.content.split(' ')
    if message.author.id == os.getenv('ADMIN'):
        com.admin_command(message, command, config)

    elif str(message.author) in p_users:
        com.p_user_command(message, command)

    else:
        com.user_command(message, command)

client.run(token)