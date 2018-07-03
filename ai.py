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
from gtts import gTTS
import os
import hashlib
import re

async def on_message(patt: u.Patt, msg: discord.Message, start_time: int):
    failed = False
    author: discord.Member = msg.author
    guild: discord.Guild = msg.guild
    channel: discord.Channel = msg.channel
    type: discord.MessageType = msg.type
    query = await get_query_text(patt, msg)
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
        context.voice = context.output
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
                except Exception:
                    failed = True
                    await msg.channel.send('`There was an error when handling that request`')
                    error = traceback.format_exc()
                    print(error)
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

    context.voice = rtn

    voice = False
    # say in voice
    if msg.channel.name.lower() == 'patt' and guild.voice_client is not None and context.voice is not None:
        if str(context.voice).strip() != '':
            try:
                voice = guild.voice_client
                voice_msg = context.voice.replace('`', '')
                p = re.compile("<(#|@[!]?|&)(\d{18})>")
                for m in p.findall(voice_msg):
                    if m[0] == "@" or m[0   ] == "@!":
                        g = patt.client.get_user(int(m[1]))
                        if g is not None:
                            voice_msg = voice_msg.replace('<{}{}>'.format(*m), g.display_name)
                    elif m[0] == '#':
                        g = patt.client.get_channel(int(m[1]))
                        if g is not None:
                            voice_msg = voice_msg.replace('<{}{}>'.format(*m), g.name)
                file = 'tts/'+hashlib.md5(voice_msg.encode()).hexdigest()+".mp3"
                if not os.path.exists(file):
                    tts = gTTS(text=voice_msg, lang='en-us')
                    tts.save(file)
                source = discord.FFmpegPCMAudio(file)
                if guild.voice_client.is_playing() == False:
                    voice.play(source)
                voice = True
            except Exception as e:
                failed = True
                error = traceback.format_exc()
                print(error)
        
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
        if voice:
            dic['Voice'] = True
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


async def get_query_text(patt: u.Patt, msg: discord.Message):

    # Remove punctuation and patt mentions
    query = msg.content \
        .replace('<@{}>'.format(patt.client.user.id), '') \
        .replace('<@!{}>'.format(patt.client.user.id), '') \
        .replace(',', '') \
        .replace('.', '') \
        .replace('?', '') \
        .replace('!', '') \
        .replace('`', '') \
        .strip()

    # Replace all mentions to new format
    for m in re.finditer(r"<(@&|@!?|#)([0-9]{18})>", query):
        mention_type = m.group(1)
        if mention_type == '@' or mention_type == '@!':
            mention_type = 'user'
        elif mention_type == '@&':
            mention_type = 'role'
        elif mention_type == '#':
            mention_type = 'channel'
        id = m.group(2)

        query = query.replace(m.group(0), '{};{}'.format(mention_type, id))
    
    return query

async def handle_payload(json: dict, context: u.IntentContext):
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
    if 'voice' in payload:
        s = payload['voice']
        if isinstance(s, list) or isinstance(s, tuple) or isinstance(s, set):
            context.voice = random.choice(s)
        else:
            context.voice = s
            if s == 'none':
                context.voice = None
    if 'voiceState' in payload:
        s = payload['voiceState']
        c: discord.VoiceClient = context.message.guild.voice_client
        if c is not None:
            if s == 'pause':
                if c.is_playing():
                    c.pause()
            elif s == 'stop':
                if c.is_playing():
                    c.stop()
            elif s == 'resume':
                if c.is_paused():
                    c.resume()
    return True


async def getJSONImage(url, name):
    async with aiohttp.request('GET', url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
