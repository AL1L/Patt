import utils as u

class Command(u.Command):
    name = "guild-amt"
    description = "Shows how many guilds I am in"
    usage = '{cmd_prefix}guild-amt'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        context.cursor.execute("SELECT * FROM guilds")
        rows = context.cursor.fetchall()
        await client.send_message(msg.channel, '<@{}>: I am in `{}` guilds'.format(msg.author.id, len(rows)))
