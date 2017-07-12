import aiohttp
import utils as u


class Command(u.Command):
    name = "ron"
    description = "Random Ron Swanson quote"
    usage = '{cmd_prefix}ron'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        url = await getJSONThing('http://ron-swanson-quotes.herokuapp.com/v2/quotes', 0)
        await client.send_message(msg.channel, '<@{}> here\'s one for ya!\n{}'.format(msg.author.id, url))


async def getJSONThing(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
