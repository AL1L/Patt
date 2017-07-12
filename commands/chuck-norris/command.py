import aiohttp
import utils as u

class Command(u.Command):
    name = "chuck-norris"
    description = "Random Chuck Norris jokes"
    usage = '{cmd_prefix}chuck-norris'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        url = await getJSONThing('https://api.chucknorris.io/jokes/random', 'value')
        await client.send_message(msg.channel, '<@{}> here\'s one for ya!\n{}'.format(msg.author.id, url))


async def getJSONThing(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
