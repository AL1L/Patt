import discord
import apiai
import json as j


async def on_message(client: discord.Client, msg: discord.Message):
    author: discord.Member = msg.author
    server: discord.Server = msg.server
    channel: discord.Channel = msg.channel
    type: discord.MessageType = msg.type
    query = msg.content[len('<@' + client.user.id + '>'):]
    ai = apiai.ApiAI('abd47900ec2845f0a5b387a0e8c8dd64')
    request = ai.text_request()
    request.session_id = author.id
    request.query = query
    response = request.getresponse()
    json = j.loads(response.read())
    rtn = json['result']['fulfillment']['speech']
    if rtn.startswith('%command:'):
        msg.content = rtn[9:]
        print(msg.content)
        await client.on_message(msg)
        return
    rtn = rtn.format(client_name=client.user.name,
                     author_mention='<@' + author.id + '>',
                     guild_name=server.name,
                     guild_users=server.member_count)
    if rtn is "" or rtn is None:
        rtn = "Sorry, i didn't understand what you said."
    await client.send_message(msg.channel, rtn)
