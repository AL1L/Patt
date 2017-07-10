import aiohttp
import utils as u


async def execute(context: u.CommandContext):
    msg = context.message
    client = context.client
    url = ".mp4"
    while url.endswith('.mp4'):
        url = await getJSONImage('https://random.cat/meow', 'file')
    await client.send_message(msg.channel, 'I got a kitten just for you <@{}>!\n{}'.format(msg.author.id, url))


async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
