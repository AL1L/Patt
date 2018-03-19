import discord
import apiai
import json as j
import utils as u
import time
import traceback


log_channel = None

async def on_message(client: discord.Client, msg: discord.Message, start_time):
    global log_channel
    if log_channel is None:
        log_channel = client.get_server("366785187029188609").get_channel('366785269351055360')
    author: discord.Member = msg.author
    server: discord.Server = msg.server
    channel: discord.Channel = msg.channel
    type: discord.MessageType = msg.type
    query = msg.content.replace('<@{}>'.format(client.user.id), '').replace(',', '').replace('.', '').replace('?', '').replace('!', '').replace('`', '').strip()
    print('FR [{}] > {}'.format(author.id, query))
    ai = apiai.ApiAI('API_KEY')
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
    rtn = rtn.replace('%author_mention%', '<@' + author.id + '>')
    rtn = rtn.replace('%client_name%', client.user.name)
    if server is not None:
        rtn = rtn.replace('%guild_name%', server.name)
        rtn = rtn.replace('%guild_users%', '{}'.format(server.member_count))
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
    
    print('TO [{}] < {}'.format(author.id, rtn))
    
    if context is not None:
        intent = u.get_intent(context.name)
        if intent is not None:
            try:
                # Execute the intent module
                await intent.handle(context)
            except Exception as e:
                failed = True
                await client.send_message(msg.channel, '`There was an error when handling that request`')
                error = traceback.format_exc()
                print(e)
        rtn = context.output
    
    if rtn is '' or rtn is None:
        rtn = ' '
    if context is not None:
        if context.output_embed is None:
            await client.send_message(msg.channel, rtn)
        else:
            await client.send_message(msg.channel, rtn, embed=context.output_embed)
    else:
        await client.send_message(msg.channel, rtn)
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
        #                     '**Server:**\n{server}\n\n' + \
        #                     '**Channel:**\n{channel}\n\n'
        embed.description = embed.description + \
                            '**Start Time:**\n{start}\n\n' + \
                            '**End Time:**\n{end}\n\n'
        if rtn.strip() is not '':
            rtn = '`' + rtn + '`'
        if context.output_embed is not None:
            rtn = rtn + '\n\n**Embed:**\ntrue'
        embed.description = embed.description.format(uid=author.id, input=query, output=rtn, start=u.format_ms_time(start_time), end=u.format_ms_time(start_time + time_took), response_id=json['id'], intent=json['result']['metadata']['intentName'] + ' (' + json['result']['metadata']['intentId'] + ')')
        embed.title = 'Got message'
        embed.color = discord.Colour.green()
        embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
        await client.send_message(log_channel, '', embed=embed)
    


async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url