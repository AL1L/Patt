import aiohttp
import discord
import utils as u

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        context.cursor.execute("SELECT * FROM guilds")
        rows = context.cursor.fetchall()
        gamt = len(rows)
        context.output = context.output.replace('%guilds%', str(gamt))
