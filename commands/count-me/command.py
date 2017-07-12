import utils as u

class Command(u.Command):
    name = "count-me"
    description = "Counts all your messages in the current channel"
    usage = '{cmd_prefix}count-me'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        counter = 0
        tmp = await client.send_message(msg.channel, 'Calculating messages...')
        async for log in client.logs_from(msg.channel, limit=100000000):
            if log.author == msg.author:
                counter += 1
        plus = ('', '+')[counter == 100]
        await client.edit_message(tmp, '<@{}>: You have {}{} messages in this channel.'.format(msg.author.id, plus, counter))
