import aiohttp
import discord
import utils as u
import os
import sys
from subprocess import check_output


allowed_users = [366085504971571200, 202150484058832905]

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        if context.message.author.id in allowed_users:
            await context.message.channel.send('Pulling...')
            context.output = '```' + check_output(["git", "pull", "https://github.com/artex-development/Patt.git", "wip/ai-dev"]).decode() + '```'
