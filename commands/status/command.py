import discord
import time
import utils as u


class Command(u.Command):
    name = "status"
    description = "A test command for the bot developer"
    usage = '{cmd_prefix}status'
    type = "none"
    permissions = ['user:152953323417239552', 'send_messages', 'read_messages']

    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        color = u.get_hex_color(discord.Colour.green())
        embed = discord.Embed()
        embed.description = 'testing'
        embed.set_author(name='{} Status'.format(context.client.user.name), icon_url='https://dummyimage.com/256x256/{color}/{color}.png'.format(color=color))
        time_took = int(round(time.time() * 1000)) - context.start_time
        embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
        await context.client.send_message(context.message.channel, '' ,embed=embed)
        return
