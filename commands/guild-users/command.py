import utils as u


async def execute(context: u.CommandContext):
    msg = context.message
    client = context.client
    await client.send_message(msg.channel,
                              '<@{}>: The guild `{}` has `{}` memebers'.format(msg.author.id, msg.server.name,
                                                                               msg.server.member_count))
