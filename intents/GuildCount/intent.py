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
        context.cursor.execute("SELECT * FROM guilds")
        rows = context.cursor.fetchall()
        gamt = len(rows)
        context.output = context.output.replace('%guilds%', str(gamt))
