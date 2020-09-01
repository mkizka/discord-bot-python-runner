import os
import re
import tempfile
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
    match = re.match(r'!py\s```py\n(.+)\n```', message.content, flags=(re.MULTILINE | re.DOTALL))
    if match:
        program = match.group(1)
        filepath = tempfile.mktemp(suffix='.py')
        with open(filepath, 'w') as f:
            f.write(program)
        try:
            process = subprocess.run(
                ['python', f'{filepath}'],
                timeout=5,
                encoding='utf-8',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            result = f'```\n{process.stderr or process.stdout}\n```'
        except Exception as e:
            result = f'実行に失敗しました\n'
            result += f'入力\n'
            result += f'```py{program}```\n'
            result += f'エラー\n'
            result += f'```{e}```'
        await message.channel.send(result)


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
