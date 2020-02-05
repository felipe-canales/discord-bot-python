import os

import discord
from dotenv import load_dotenv

import commands as com
from config import load_p_users

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    global p_users
    print(f'{client.user} has connected to Discord!')
    print("Loading p-users...")
    p_users = load_p_users()


@client.event
async def on_message(message):
    if message.content[0:3].lower() != "trz":
        return
    
    command = message.content.split(' ')
    if str(message.author) == os.getenv('ADMIN'):
        com.admin_command(command)

    elif str(message.author) in p_users:
        com.p_user_command(command)

    else:
        com.user_command(command)

client.run(token)