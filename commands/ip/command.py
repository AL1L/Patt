import aiohttp
import discord
import time
import utils as u

class Command(u.Command):
    name = "ip"
    description = "Get info about an IP address or domain"
    usage = '{cmd_prefix}ip <ip|domain>'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        lang = u.lang(context.name, context.message.author)
        if len(context.args) < 1:
            await context.client.send_message(context.message.channel, lang['missing_arg_0'].format(user_id=context.message.author.id))
        async with aiohttp.get('http://ip-api.com/json/' + context.args[0]) as r:
            if r.status == 200:
                json = await r.json()
                
                if json['status'] != 'success':
                    await context.client.send_message(context.message.channel, 'IP address not found.')
                    return
            
                title = lang['title']
                title = title.format(user_id=context.message.author.id, ip=json['query'])
            
                message = ''
                message += '**Location:**' + '\n' + json['city'] + ', ' + json['regionName'] + ' ' + json['zip'] + ' ' + json['countryCode'] + '\n\n'
                message += '**ISP:**' + '\n' + json['isp'] + '\n\n'
                message += '**Organization:**' + '\n' + json['org'] + '\n\n'
                message += '**AS number/name:**' + '\n' + json['as'] + '\n\n'
            
                embed = discord.Embed()
                embed.color = discord.Colour.gold()
                embed.title = title
                embed.description = message
            
                embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
                
                time_took = int(round(time.time() * 1000)) - context.start_time
                embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))
            
                await context.client.send_message(context.message.channel, '', embed=embed)


async def getJSONImage(url, name):
    async with aiohttp.get(url) as r:
        if r.status == 200:
            js = await r.json()
            url = js[name]
            return url
