import os

import discord
from dotenv import load_dotenv

from commands import process_command#, admin_command, p_user_command, user_command, 
from parser import parse_msg
from config import Config

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guild_messages = True
client = discord.Client(intents=intents)
cfg = Config()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    print(message.content)
    if message.content[0:3].lower() != "svr":
        return

    command = parse_msg(message.content.lower(), message.clean_content)

    if message.author.id == int(os.getenv('ADMIN')):
        if command[0] == "shut":
            cfg.save_p_users()
            await message.channel.send("Shutting down :(")
            await client.close()
            return
        await message.channel.send(process_command(command, cfg, 0, True))

    else:
        await message.channel.send(process_command(command, cfg, str(message.author.id)))

client.run(token)
