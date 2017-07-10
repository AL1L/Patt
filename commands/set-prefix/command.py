async def execute(context):
    msg = context.message
    client = context.client
    if msg.author.id != msg.server.owner.id:
        await client.send_message(msg.channel, '<@{}>: Only the guild owner may run this command!'.format(msg.author.id))
        return
    if context.args[1] is None:
        await client.send_message(msg.channel, '<@{}>: You must specify a prefix!'.format(msg.author.id))
        return
    context.cursor.execute("UPDATE guilds SET prefix='{}' WHERE gid='{}'".format(context.args[1], msg.server.id))
    context.database.commit()
    await client.send_message(msg.channel, '<@{}>: The guild `{}` prefix has been set to `{}`'.format(msg.author.id, msg.server.name, context.args[1]))
