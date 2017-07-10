import aiohttp
import discord
import time
import utils as u


async def execute(context: u.CommandContext):
    msg = context.message
    client = context.client
    url = ".mp4"
    while url.endswith('.mp4'):
        url = await getJSONImage('https://random.dog/woof.json', 'url')

    lang = u.lang(context.name, context.message.author)

    title = lang['title']
    title = title.format(user_id=context.message.author.id)

    time_took = int(round(time.time() * 1000)) - context.start_time

    embed = discord.Embed()
    embed.color = discord.Colour.gold()
    embed.title = title

    embed.set_image(url=url)
    embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
    embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))

    await context.client.send_message(context.message.channel, '', embed=embed)


async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
