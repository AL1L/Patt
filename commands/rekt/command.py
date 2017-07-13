import aiohttp
import discord
import time
import utils as u


class Command(u.Command):
    name = "rekt"
    description = "Useful when someone gets _totally_ **REKT**"
    usage = '{cmd_prefix}rekt'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        context.args = context.args[1:]
        message = ""
        for string in context.args:
            message = message + string + " "
        lang = u.lang(context.name, context.message.author)

        title = lang['title']
        title = title.format(user_id=context.message.author.id)

        time_took = int(round(time.time() * 1000)) - context.start_time

        embed = discord.Embed()
        embed.color = discord.Colour.gold()
        embed.title = title

        embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
        embed.set_image(url=lang['image_url'])
        embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))

        await context.client.send_message(context.message.channel, message, embed=embed)
