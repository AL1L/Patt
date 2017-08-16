import discord
import utils as u
from datetime import datetime, timedelta


class Command(u.Command):
    name = "test"
    description = "A test command for the bot developer"
    usage = '{cmd_prefix}purge {ammount} [user]'
    type = "none"
    permissions = ['manage_messages', 'send_messages', 'read_messages']

    @staticmethod
    async def execute(context: u.CommandContext):
        d = datetime.today() - timedelta(days=14)
        if len(context.args) > 0:
            def check(msg):
                if len(context.args) > 1:
                    return context.args[1][2:][:1] == msg.author.id
                else:
                    return True
            
            deleted = await context.client.purge_from(context.message.channel, limit=int(context.args[0]), check=check, after=d)
            await context.client.send_message(context.message.channel, 'Deleted {} message(s)'.format(len(deleted)))
        return
