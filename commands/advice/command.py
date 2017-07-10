import aiohttp

async def execute(context):
    msg = context.message
    client = context.client
    async with aiohttp.get('http://api.adviceslip.com/advice') as r:
        if r.status == 200:
            js = await r.json()
            await client.send_message(msg.channel, '<@{}> here\'s slip number {}\n{}'.format(msg.author.id, js['slip']['slip_id'], js['slip']['advice']))
