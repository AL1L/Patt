import aiohttp

async def execute(context):
    msg = context.message
    client = context.client
    url = ".mp4"
    while url.endswith('.mp4'):
        url = await getJSONImage('https://random.dog/woof.json', 'url')
    await client.send_message(msg.channel, 'I got a doggo just for you <@{}>!\n{}'.format(msg.author.id, url))
    
async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
