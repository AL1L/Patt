async def execute(context):
    msg = context.message
    client = context.client
    counter = 0
    tmp = await client.send_message(msg.channel, 'Calculating messages...')
    async for log in client.logs_from(msg.channel, limit=100000000):
        if log.author == msg.author:
            counter += 1
    plus = ('', '+')[counter == 100]
    await client.edit_message(tmp, '<@{}>: You have {}{} messages in this channel.'.format(msg.author.id, plus, counter))
