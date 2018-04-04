import discord
import apiai
import json as j
import utils as u
import time
import traceback
import sys
import json as jsonlib
import random
import aiohttp


async def on_message(patt: u.Patt, msg: discord.Message, start_time: int):
    failed = False
    author: discord.Member = msg.author
    guild: discord.Guild = msg.guild
    channel: discord.Channel = msg.channel
    type: discord.MessageType = msg.type
    query = msg.content \
        .replace('<@{}>'.format(patt.client.user.id), '') \
        .replace('<@!{}>'.format(patt.client.user.id), '') \
        .replace(',', '') \
        .replace('.', '') \
        .replace('?', '') \
        .replace('!', '') \
        .replace('`', '') \
        .strip()
    print('FR [{}] > {}'.format(author.id, query))
    ai = apiai.ApiAI(patt.apiai_token)
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
    rtn = rtn.replace('%client_name%', patt.client.user.name)
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
        context.patt = patt
        context.message = msg
        context.start_time = start_time
        context.request = json
        context.user = u.get_user(patt, msg.author.id)

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
    # Log

    if context is not None and patt.log_channel is not None:
        time_took = int(round(time.time() * 1000)) - start_time
        content = ''
        color = None
        thumb = None
        if rtn.strip() is not '':
            rtn = '`' + rtn.replace('`', '\\`') + '`'
        dic = {
            'Id': json['id'],
            'Intent': '`'+json['result']['metadata']['intentName'] + '` (' + json['result']['metadata']['intentId'] + ')',
            'Start Time': u.format_ms_time(start_time),
            'End Time': u.format_ms_time(start_time + time_took),
            'Input': '`'+query+'`',
            'Output': rtn
        }
        if context.output_embed is not None:
            dic['Embed'] = True
        if isinstance(msg.channel, discord.abc.GuildChannel):
            dic['Guild'] = '`' + msg.guild.name + \
                '` (' + str(msg.guild.id) + ')'
            dic['Channel'] = '`' + msg.channel.name + \
                '` (<#' + str(msg.channel.id) + '>)'
            thumb = msg.guild.icon_url
        if failed:
            content = '<@&425476747165827083>'
            dic['Error'] = '```'+error.replace('`', '\\`')+'```'
            color = discord.Colour.red()
        await u.log(patt, dic, title="Got message", content=content, color=color, footer="\U000023F3 Took {}ms".format(time_took), author=author, thumbnail=thumb)


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
    async with aiohttp.request('GET', url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
