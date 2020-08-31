import os
import subprocess
import discord

client = discord.Client()


@client.event
async def on_ready():
    print('ログイン完了')


@client.event
async def on_message(message: discord.Message) -> None:
    suffix = '!py\n'
    if message.author.bot:
        return
    if message.content.startswith(suffix):
        program = message.content[len(suffix):]
        process = subprocess.run(
            ['python', '-c', f'{program}'],
            timeout=5,
            encoding='utf-8',
            stdout=subprocess.PIPE
        )
        await message.channel.send(process.stdout.strip())


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
