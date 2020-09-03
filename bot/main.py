import os
import re
from urllib import parse

import docker
from docker.errors import ContainerError
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
        try:
            result = run_docker_python(program)
            if not parse.urlparse(result).scheme:
                result = f'```\n{result[:500]}\n```'
        except ContainerError as e:
            error = e.stderr.decode('utf-8')
            if error:
                result = f'```\n{error[:500]}\n```'
            else:
                result = '`エラー出力が空だったか、タイムアウトしました`'
        await message.channel.send(result)


def run_docker_python(program: str) -> str:
    docker_client = docker.from_env()
    result = docker_client.containers.run(
        image='python:3.8-slim',
        environment={
            'PROGRAM': program
        },
        command=f'bash -c \"echo \\"$PROGRAM\\" > run.py && timeout 5 python run.py\"',
        working_dir='/code',
        remove=True
    )
    return result.decode('utf-8')


if __name__ == '__main__':
    TOKEN = os.environ['TOKEN']
    client.run(TOKEN)
