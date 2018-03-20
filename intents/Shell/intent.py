import aiohttp
import discord
import utils as u
import os
import sys
import subprocess


allowed_users = [366085504971571200, 202150484058832905]

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        if context.message.author.id in allowed_users:
            try:
                # await context.message.channel.send('Pulling...')
                # context.output = '```' + check_output(["git", "pull", "https://github.com/artex-development/Patt.git", "wip/ai-dev"]).decode() + '```'
                client = context.client
                cmd = context.raw_input.replace('<@{}>'.format(client.user.id), '').replace('<@!{}>'.format(client.user.id), '').strip()[1:].strip().split(' ')
                print(cmd)
                context.output = '```' + subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode() + '```'
            except Exception as e:
                context.output = 'There was an error: `'+str(e)+'`'
