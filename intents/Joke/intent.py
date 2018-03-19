import aiohttp
import discord
import utils as u


class Intent(u.Intent):

    @staticmethod
    async def handle(context: u.IntentContext):
        joke = await getJSONText('https://icanhazdadjoke.com/', 'joke')
        
        context.output = joke

async def getJSONText(url, name):
    hd = {'Accept':'application/json'}
    async with aiohttp.get(url, headers=hd) as r:
        print(r.headers['Content-Type'])
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
