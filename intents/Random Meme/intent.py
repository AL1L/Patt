import aiohttp
import discord
import utils as u


class Intent(u.Intent):

    @staticmethod
    async def handle(context: u.IntentContext):
        url = await getJSONImage('https://meme-api.explosivenight.us/v1/random/?type=json', 'url')
        
        embed = discord.Embed()
        embed.color = discord.Colour.gold()
        embed.title = 'Here\'s a meme for ya!'
        embed.set_image(url=url)
        embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
        embed.set_footer(text='Powered by https://meme-api.explosivenight.us/')

        context.output = ""
        context.output_embed = embed

async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
