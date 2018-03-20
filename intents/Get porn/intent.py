import aiohttp
import discord
import utils as u
import random
import re

class Intent(u.Intent):

    @staticmethod
    async def handle(context: u.IntentContext):
        
        porn_type = context.request['result']['parameters']['nsfw_type']
        
        if porn_type == '':
            context.output = 'I don\'t know what those are, try asking for something else'
            return
        
        url = await getImage(porn_type)
        
        embed = discord.Embed()
        embed.color = discord.Colour.gold()
        embed.set_image(url=url)

        context.output = getTitle(porn_type)
        context.output_embed = embed

def getTitle(type):
    return random.choice({
        'tiny-tits': [
            "I guess i can show you this one, don't judge my size",
            "They're a little small, but what do you think?"
        ],
        "pussy": [
            "Looks tasty doesn't it?",
            "Ooh I'd love to eat this one out"
        ],
        "big-cock": [
            "Oh my it's so big, i just want to sit on it all day!",
            "Looks like this one needs to be sucked ;)"
        ],
        "ass": [
            "Dat ass tho!",
            "Take a look at this nice ass"
        ],
        "self-shot": [
            "Isn't she cute?",
            "Oh i love her?",
            "I'd smash"
        ],
        "big-tits": [
            "Look at these babies",
            "Mmm, so big, just how I like it."
        ],
        "babe": [
            "Isn't she cute?",
            "Oh i love her?",
            "I'd smash"
        ]
    }[type])

async def getImage(type):
    num = str(random.randint(1, 40))
    url = 'https://www.pornpics.com/'+type+'/'+type+'-'+num+'.shtml'
    print(url)
    async with aiohttp.request('GET', url) as r:
        if r.status == 200:
            text = await r.text()
            p = re.compile("<img srcset='(https://(www|content|img)\.pornpics\.com/[0-9-]{10}/[0-9]+_[0-9]+\.(jpg|png|gif)) 300w")
            
            
            return p.search(text).group(1)
