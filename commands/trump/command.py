import aiohttp
import utils as u


async def execute(context: u.CommandContext):
    msg = context.message
    client = context.client
    url = await getJSONThing('https://api.tronalddump.io/random/quote', 'value')
    await client.send_message(msg.channel, '<@{}> Sir the president wanted to say...\n{}'.format(msg.author.id, url))


async def getJSONThing(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
