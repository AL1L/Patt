import aiohttp
import utils as u


async def execute(context: u.CommandContext):
    session = aiohttp.ClientSession()
    async with session.get('http://api.adviceslip.com/advice') as r:
        if r.status == 200:
            js = await r.json()
            await context.client.send_message(context.message.channel, '<@{}> here\'s slip number {}\n{}'
                                              .format(context.message.author.id, js['slip']['slip_id'],
                                                      js['slip']['advice']))
    session.close()
