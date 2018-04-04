import aiohttp
import discord
import utils as u
import re


class Intent(u.Intent):

    @staticmethod
    async def handle(context: u.IntentContext):
        patt = context.patt
        if patt.oxford_dictionaries['id'] is None or patt.oxford_dictionaries['key'] is None:
            return
        
        word = context.request['result']['parameters']['any']
        regex = re.compile('[^a-zA-Z]')
        word = regex.sub('', word)
        headers = {
            "Accept": "application/json",
            "app_id": patt.oxford_dictionaries['id'],
            "app_key": patt.oxford_dictionaries['key']
        }
        async with aiohttp.request('GET', 'https://od-api.oxforddictionaries.com/api/v1/entries/en/'+word, headers=headers) as r:
            if r.status == 200:
                js = await r.json()
                deff = js['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
                
                context.output = "The word `" + word + "` is defined as " + deff