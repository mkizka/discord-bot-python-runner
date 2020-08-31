import os
import subprocess
import discord

client = discord.Client()


@client.event
async def on_ready():
    print('ログイン完了')


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    if message.content == '!py':
        await message.channel.send('hoge')


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
