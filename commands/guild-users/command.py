import utils as u


class Command(u.Command):
    name = "guild-users"
    description = "Shows how many users are in the current guild"
    usage = '{cmd_prefix}guild-users'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        await client.send_message(msg.channel,
                                  '<@{}>: The guild `{}` has `{}` memebers'.format(msg.author.id, msg.server.name,
                                                                                   msg.server.member_count))
