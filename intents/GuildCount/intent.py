import aiohttp
import discord
import utils as u

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        context.output = context.output.replace('%guilds%', str(len(context.patt.client.guilds)))
