import discord
import time
import utils as u
import os
import sys
from subprocess import Popen


class Command(u.Command):
    name = "test"
    description = "A test command for the bot developer"
    usage = '{cmd_prefix}test'
    type = "none"
    permissions = ['user:152953323417239552', 'channel:314442420794294272', 'send_messages', 'read_messages']

    @staticmethod
    async def execute(context: u.CommandContext):
        await context.client.send_message(context.message.channel, 'Restarting...')
        context.client.logout() 
        os.system('cls')
        Popen("bot.bat")
        sys.exit()
        return
