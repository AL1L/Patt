import aiohttp
import discord
import utils as u
import os
import sys
from subprocess import check_output


allowed_users = ['366085504971571200', '202150484058832905']

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        if context.message.author.id in allowed_users:
            await context.client.send_message(context.message.channel, 'Pulling...')
            context.output = '```' + check_output("git pull").decode() + '```'
