import aiohttp
import discord
import utils as u


class Intent(u.Intent):

    @staticmethod
    async def handle(context: u.IntentContext):
        url = await getJSONImage('http://thecatapi.com/api/images/get', 'url')
        
        embed = discord.Embed()
        embed.color = discord.Colour.gold()
        embed.title = 'Here\'s a kit kat for ya!'
        embed.set_image(url=url)
        embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)

        context.output = ""
        context.output_embed = embed

async def getJSONImage(url, name):
    async with aiohttp.request('GET', url) as r:
        if r.status == 200:
            print(r.text())
            return r.url
