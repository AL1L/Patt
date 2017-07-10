import aiohttp
import utils as u


async def execute(context: u.CommandContext):
    msg = context.message
    client = context.client
    async with aiohttp.get("https://www.theartex.net/cloud/api/?sec=announcements") as r:
        if r.status == 200:
            js = await r.json()
            await client.send_message(msg.channel,
                                      '<@{}>: Here is the latest announcement on https://theartex.net/\nTimestamp:\n {}\n\nMessage:\n{}'.format(
                                          msg.author.id, js['data'][0]['trn_date'], js['data'][0]['message']))
