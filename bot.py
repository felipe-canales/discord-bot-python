import os

import discord
from dotenv import load_dotenv

from commands import admin_command, p_user_command, user_command
from parser import parse_msg
from config import Config

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()
cfg = Config()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.content[0:3].lower() != "trz":
        return
    
    command = parse_msg(message.content)

    if message.author.id == int(os.getenv('ADMIN')):
        if message.content.lower() == "trz shut":
            cfg.save_p_users()
            await message.channel.send("Shutting down :(")
            await client.close()
            return
        await message.channel.send(admin_command(message, command, cfg))

    elif cfg.check_p_user(message.author.id):
        await message.channel.send(p_user_command(message, command))

    else:
        await message.channel.send(user_command(message, command))

client.run(token)