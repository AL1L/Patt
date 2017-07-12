import aiohttp
import discord
import time
import utils as u


class Command(u.Command):
    name = "advice"
    description = "Some helpful random advice."
    usage = '{cmd_prefix}advice'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        session = aiohttp.ClientSession()
        async with session.get('http://api.adviceslip.com/advice') as r:
            if r.status == 200:
                js = await r.json()

                lang = u.lang(context.name, context.message.author)

                message = '\n' + lang['slip_number_label'] + '\n' + lang['slip_number'] + '\n\n' + lang[
                    'slip_message_label'] + \
                          '\n' + lang['slip_message']
                message = message.format(user_id=context.message.author.id, slip_id=js['slip']['slip_id'],
                                         slip_message=js[
                                             'slip']['advice'])

                title = lang['title']
                title = title.format(user_id=context.message.author.id, slip_id=js['slip']['slip_id'], slip_message=js[
                    'slip']['advice'])

                time_took = int(round(time.time() * 1000)) - context.start_time

                embed = discord.Embed()
                embed.color = discord.Colour.green()
                embed.title = title
                embed.description = message

                embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
                embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))

                await context.client.send_message(context.message.channel, '', embed=embed)
        session.close()
        return
