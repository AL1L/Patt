import aiohttp
import discord
import utils as u
import os
import sys
from subprocess import Popen


allowed_users = ['366085504971571200', '202150484058832905']

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        print(type(context.message.author.id))
        if context.message.author.id in allowed_users:
            await context.client.send_message(context.message.channel, 'I\'m goning to take a quick power-nap and I\'ll be right back!')
            context.client.logout() 
            os.system('cls')
            Popen("bot.bat")
            sys.exit()
            return
