import discord
import apiai
import json as j
import utils as u
import time
import traceback
import sys
import json as jsonlib
import random


# Test comment

log_channel = None

async def on_message(client: discord.Client, cur, msg: discord.Message, start_time):
    global log_channel
    failed = False
    if log_channel is None:
        log_channel = client.get_guild(366785187029188609).get_channel(366785269351055360)
    author: discord.Member = msg.author
    guild: discord.Guild = msg.guild
    channel: discord.Channel = msg.channel
    type: discord.MessageType = msg.type
    query = msg.content.replace('<@{}>'.format(client.user.id), '').replace('<@!{}>'.format(client.user.id), '').replace(',', '').replace('.', '').replace('?', '').replace('!', '').replace('`', '').strip()
    print('FR [{}] > {}'.format(author.id, query))
    ai = apiai.ApiAI(sys.argv[2])
    request = ai.text_request()
    request.session_id = author.id
    request.query = query
    response = request.getresponse()
    json_raw = response.read()
    json = j.loads(json_raw)
    rtn = json['result']['fulfillment']['speech']
    if 'result' in json:
        if 'action' in json['result']:
            action = json['result']['action']
    rtn = rtn.replace('%author_id%', '{author_id}')
    rtn = rtn.replace('%author_mention%', '<@' + str(author.id) + '>')
    rtn = rtn.replace('%client_name%', client.user.name)
    if guild is not None:
        rtn = rtn.replace('%guild_name%', guild.name)
        rtn = rtn.replace('%guild_users%', '{}'.format(guild.member_count))
    if rtn is "" or rtn is None:
        rtn = "Sorry, i didn't understand what you said."
    
    context = None
    if 'intentName' in json['result']['metadata']:
        context = u.IntentContext()
        context.name = json['result']['metadata']['intentName']
        context.id = json['result']['metadata']['intentId']
        context.input = query
        context.raw_input = msg.content
        context.output = rtn
        context.client = client
        context.message = msg
        context.start_time = start_time
        context.cursor = cur
        context.request = json
    
    if context is not None:
        if await handle_payload(json, context):
            intent = u.get_intent(context.name)
            if intent is not None:
                try:
                    # Execute the intent module
                    await intent.handle(context)
                except Exception as e:
                    failed = True
                    await msg.channel.send('`There was an error when handling that request`')
                    error = traceback.format_exc()
                    print(e)
        rtn = context.output
    
    print('TO [{}] < {}'.format(author.id, rtn))
    if rtn is '' or rtn is None:
        rtn = ' '
    if context is not None:
        if context.output_embed is None:
            await msg.channel.send(rtn)
        else:
            await msg.channel.send(rtn, embed=context.output_embed)
    else:
        await msg.channel.send(rtn)
   # print(json_raw)
    # Log
    
    if context is not None:
        time_took = int(round(time.time() * 1000)) - start_time
        embed = discord.Embed()
        embed.description = '**User:**\n<@{uid}> ({uid})\n\n' + \
                            '**Input:**\n`{input}`\n\n' + \
                            '**Output:**\n{output}\n\n' + \
                            '**Id:**\n{response_id}\n\n' + \
                            '**Intent:**\n`{intent}`\n\n'
        # embed.description = embed.description + \
        #                     '**Guild:**\n{guild}\n\n' + \
        #                     '**Channel:**\n{channel}\n\n'
        embed.description = embed.description + \
                            '**Start Time:**\n{start}\n\n' + \
                            '**End Time:**\n{end}\n\n'
        if rtn.strip() is not '':
            rtn = '`' + rtn.replace('`', '') + '`'
        if context.output_embed is not None:
            rtn = rtn + '\n\n**Embed:**\ntrue'
        embed.description = embed.description.format(uid=author.id, input=query, output=rtn, start=u.format_ms_time(start_time), end=u.format_ms_time(start_time + time_took), response_id=json['id'], intent=json['result']['metadata']['intentName'] + ' (' + json['result']['metadata']['intentId'] + ')') 
        embed.title = 'Got message'
        au = author.display_name + '#' + author.discriminator
        embed.set_author(name=au, icon_url=author.avatar_url)
        content = ''
        if failed:
            content = '<@&425476747165827083>'
            embed.color = discord.Colour.red()
            embed.description = embed.description + '**Error:**\n```{}```\n\n'.format(error)
        else:
            embed.color = discord.Colour.green()
        embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
        await log_channel.send(content, embed=embed)
    
async def handle_payload(json, context):
    # print(jsonlib.dumps(json))
    # Make sure there is a payload
    if 'result' not in json: 
        return
    if 'fulfillment' not in json['result']: 
        return
    if 'messages' not in json['result']['fulfillment']: 
        return
    payload = None
    for msg in json['result']['fulfillment']['messages']:
        if msg['type'] != 4:
            continue
        payload = msg['payload']
    if payload is None:
        return True
        
    # Do stuff
    if 'nsfw' in payload and not context.message.channel.is_nsfw():
        context.output = random.choice(payload['nsfw'])
        return False
    return True

async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
