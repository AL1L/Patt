import utils as u


class Command(u.Command):
    name = "set-prefix"
    description = "Sets the current guild's command prefix."
    usage = '{cmd_prefix}set-prefix'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        if len(context.args) < 2:
            await client.send_message(msg.channel, '<@{}>: You must specify a prefix!'.format(msg.author.id))
            return
        context.cursor.execute("UPDATE guilds SET prefix='{}' WHERE gid='{}'".format(context.args[1], msg.server.id))
        context.database.commit()
        await client.send_message(msg.channel,
                                  '<@{}>: The guild `{}` prefix has been set to `{}`'.format(msg.author.id,
                                                                                             msg.server.name,
                                                                                             context.args[1]))
