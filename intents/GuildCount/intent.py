import aiohttp
import discord
import utils as u

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        context.patt.cursor.execute("SELECT * FROM guilds")
        rows = context.patt.cursor.fetchall()
        gamt = len(rows)
        context.output = context.output.replace('%guilds%', str(gamt))
