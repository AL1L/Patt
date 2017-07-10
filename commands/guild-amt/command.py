import utils as u


async def execute(context: u.CommandContext):
    msg = context.message
    client = context.client
    context.cursor.execute("SELECT * FROM guilds")
    rows = context.cursor.fetchall()
    await client.send_message(msg.channel, '<@{}>: I am in `{}` guilds'.format(msg.author.id, len(rows)))
