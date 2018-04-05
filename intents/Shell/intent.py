import aiohttp
import discord
import utils as u
import os
import sys
import subprocess
import time


allowed_users = [366085504971571200, 202150484058832905]

class Intent(u.Intent):
    
    @staticmethod
    async def handle(context: u.IntentContext):
        patt: u.Patt = context.patt
        if context.message.author.id in allowed_users:

            embed = discord.Embed()
            embed.title = "Shell"
            embed.color = discord.Colour.green()
            
            client = context.patt.client
            cmd = context.raw_input.replace('<@{}>'.format(client.user.id), '').replace('<@!{}>'.format(client.user.id), '').strip()[1:].strip()
        
            if cmd == 'join':
                author = context.message.author
                if author.voice is None:
                    context.output = 'Not in voice channel!'
                    return
                if context.message.guild.voice_client is not None:
                    context.output = 'Already joined'
                    return
                channel = await author.voice.channel.connect()
                context.output = 'Joined'
                return
            if cmd == 'leave':
                author = context.message.author
                if context.message.guild.voice_client is None:
                    context.output = 'Not in voice channel'
                    return
                channel = await context.message.guild.voice_client.disconnect()
                context.output = 'Disconnected'
                return
            output = ""
            try:
                if cmd.startswith('eval '):
                    embed.title = "Evaluate"
                    output = str(eval(cmd[5:]))
                else:
                    output = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE).stdout.decode()
            except Exception as e:
                output = 'Error: ' + str(e)
                embed.color = discord.Colour.red()
                
            embed.description = "\n`{}` = \n```\n{}\n```\n".format(cmd, output)
            embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
            time_took = int(round(time.time() * 1000)) - context.start_time
            embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
            context.output = ""
            context.output_embed = embed
