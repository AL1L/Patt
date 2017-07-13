import time

sk_start_time = int(round(time.time() * 1000))

import discord
import utils as u
import logging
import sys
import traceback
import sqlite3 as lite
import importlib
import ai


if __name__ == "__main__":
    # Create Discord client
    client = discord.Client()


# When bot is ready
@client.event
async def on_ready():
    print('------------------------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------------------')
    await client.change_presence(game=discord.Game(name='Say @Patt for prefix'))
    log_channel = client.get_server("267529399656513538").get_channel('334544903872839682')
    time_took = int(round(time.time() * 1000)) - sk_start_time
    embed = discord.Embed()
    embed.description = '**Start Time:**\n{start}\n\n' + \
                        '**Ready At:**\n{end}\n\n'
    embed.description = embed.description.format(start=u.format_ms_time(sk_start_time),
                                                 end=u.format_ms_time(sk_start_time + time_took))
    embed.title = 'Bot Started'
    embed.color = discord.Colour.green()
    embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
    await client.send_message(log_channel, '', embed=embed)


# When a message is sent that can be read by Patt
@client.event
async def on_message(msg):
    # Start Time
    start_ms_time = int(round(time.time() * 1000))

    # Channel cannot be private
    if msg.channel.is_private:
        return

    # Get the server from the database
    cur.execute("SELECT * FROM guilds WHERE gid='{}'".format(msg.server.id))

    # Get the returned row
    row = cur.fetchone()

    # If the server for som reason wasn't found, set the default prefix.
    if row is None:
        prefix = '!'
    else:
        prefix = row[1]

    # If the message is '@Patt' send the guild prefix
    if msg.content == '<@{}>'.format(client.user.id):
        await client.delete_message(msg)
        await client.send_typing(msg.channel)
        await client.send_message(msg.channel, u.lang('', msg.author)['guild_prefix'].format(user_id=msg.author.id,
                                                                                             cmd_prefix=prefix))
        return
    elif msg.content.startswith('<@{}>'.format(client.user.id)):
        importlib.reload(ai)
        await ai.on_message(client, msg)
        return

    # Else, check if the message was sent with the required prefix
    elif msg.content.startswith(prefix):
        msgParts = msg.content.split(' ')
        msgParts[0] = msgParts[0][len(prefix):]
        if len(msgParts[0]) > 100:
            return
        elif not msgParts[0].replace('-', '').isalnum():
            return

        # Create command context
        context = u.CommandContext()
        context.client = client
        context.message = msg
        context.args = msgParts[1:]
        context.cursor = cur
        context.database = db
        context.name = msgParts[0]
        context.client_server_data = row
        context.start_time = start_ms_time

        command = u.get_command(context.name)

        if command is None:
            return

        await client.delete_message(msg)
        await client.send_typing(msg.channel)

        # Check permissions
        has_perm = u.has_permission(context.name, context.message)
        failed = False
        error = "None"
        if has_perm[0]:
            try:
                # Execute the command module
                await command.execute(context)
            except Exception as e:
                failed = True
                await client.send_message(msg.channel, '<@{}>: There was an error! `{}`'.format(msg.author.id, e))
                error = traceback.format_exc()
        else:
            await client.send_message(msg.channel, '<@{}>: Lacking permission `{}`'.format(msg.author.id, has_perm[1]))

        # Log the command
        log = 'CMD "{}#{}" ({}) ran "{}" on the guild "{}" ({})'.format(msg.author.name, msg.author.discriminator,
                                                                        msg.author.id, msgParts[0], msg.server.name,
                                                                        msg.server.id)
        print(log)
        time_took = int(round(time.time() * 1000)) - context.start_time

        embed = discord.Embed()
        embed.color = discord.Colour.green()
        log_channel = client.get_server("267529399656513538").get_channel('334544903872839682')
        perms = str(has_perm[0])
        if not has_perm[0]:
            perms = perms + ' ({})'.format(has_perm[1])
            embed.color = discord.Colour.orange()

        embed.description = '**Command:**\n{cmd_name}\n\n' + \
                            '**Args:**\n{cmd_args}\n\n' + \
                            '**Has Permission:**\n{has_perms}\n\n' + \
                            '**Author:**\n{author}\n\n' + \
                            '**Server:**\n{server}\n\n' + \
                            '**Channel:**\n{channel}\n\n' + \
                            '**Raw:**\n```{raw}```\n\n' + \
                            '**Start Time:**\n{start}\n\n' + \
                            '**End Time:**\n{end}'
        if failed:
            embed.color = discord.Colour.red()
            embed.description = embed.description + '\n\n**Error:**\n```{error}```'
        embed.description = embed.description.format(cmd_name=context.name, cmd_args=context.args,
                                                     author='`{author_name}#{author_discriminator}` _({author_id})_',
                                                     server='`{server_name}` _({server_id})_',
                                                     channel='`{channel_name}` _({channel_id})_', raw=msg.content,
                                                     start=u.format_ms_time(start_ms_time),
                                                     end=u.format_ms_time(start_ms_time + time_took),
                                                     has_perms=perms, error=error)
        embed.description = embed.description.format(author_name=msg.author.name,
                                                     author_discriminator=msg.author.discriminator,
                                                     author_id=msg.author.id, server_name=msg.server.name,
                                                     server_id=msg.server.id, channel_name=msg.channel.name,
                                                     channel_id=msg.channel.id)
        embed.title = 'Command Ran'
        embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
        await client.send_message(log_channel, '', embed=embed)


# When Patt joins a server
@client.event
async def on_server_join(svr):
    start_time = int(round(time.time() * 1000))
    cur.execute("INSERT INTO guilds VALUES('{}', 'p!')".format(svr.id))
    db.commit()
    time_took = int(round(time.time() * 1000)) - start_time
    log_channel = client.get_server("267529399656513538").get_channel('334544903872839682')
    embed = discord.Embed()
    embed.description = '**Server:**\n{server}\n\n' + \
                        '**Owner:**\n{owner}\n\n' + \
                        '**Users:**\n{user_amt}\n\n' + \
                        '**Is Large:**\n{is_large}\n\n' + \
                        '**Start Time:**\n{start}\n\n' + \
                        '**End Time:**\n{end}\n\n'
    embed.description = embed.description.format(owner='`{owner_name}#{owner_discriminator}` _({owner_id})_',
                                                 server='`{server_name}` _({server_id})_',
                                                 start=u.format_ms_time(start_time),
                                                 end=u.format_ms_time(start_time + time_took),
                                                 is_large=svr.large,
                                                 user_amt=len(svr.members))
    embed.description = embed.description.format(owner_name=svr.owner.name,
                                                 owner_discriminator=svr.owner.discriminator,
                                                 owner_id=svr.owner.id, server_name=svr.name,
                                                 server_id=svr.id)
    embed.set_thumbnail(url=svr.icon_url)
    embed.title = 'Added to Guild'
    embed.color = discord.Colour.green()
    embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
    await client.send_message(log_channel, '', embed=embed)


# When Patt leaves a server
@client.event
async def on_server_remove(svr):
    start_time = int(round(time.time() * 1000))
    cur.execute("DELETE FROM guilds WHERE gid='{}'".format(svr.id))
    db.commit()
    time_took = int(round(time.time() * 1000)) - start_time
    log_channel = client.get_server("267529399656513538").get_channel('334544903872839682')
    embed = discord.Embed()
    embed.description = '**Server:**\n{server}\n\n' + \
                        '**Owner:**\n{owner}\n\n' + \
                        '**Users:**\n{user_amt}\n\n' + \
                        '**Is Large:**\n{is_large}\n\n' + \
                        '**Start Time:**\n{start}\n\n' + \
                        '**End Time:**\n{end}\n\n'
    embed.description = embed.description.format(owner='`{owner_name}#{owner_discriminator}` _({owner_id})_',
                                                 server='`{server_name}` _({server_id})_',
                                                 start=u.format_ms_time(start_time),
                                                 end=u.format_ms_time(start_time + time_took),
                                                 is_large=svr.large,
                                                 user_amt=len(svr.members))
    embed.description = embed.description.format(owner_name=svr.owner.name,
                                                 owner_discriminator=svr.owner.discriminator,
                                                 owner_id=svr.owner.id, server_name=svr.name,
                                                 server_id=svr.id)
    embed.set_thumbnail(url=svr.icon_url)
    embed.title = 'Removed from Guild'
    embed.color = discord.Colour.red()
    embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
    await client.send_message(log_channel, '', embed=embed)


if __name__ == "__main__":    
    print('------------------------------')
    print('Parameters: {}'.format(sys.argv))
    
    if sys.argv[1] is None:
        print('------------------------------')
        print('Please specify a token for the bot to use.')
        quit(1)
    
    # DB setup
    db = lite.connect('db.db')
    
    cur = db.cursor()
    cur.execute('SELECT SQLITE_VERSION()')
    
    data = cur.fetchone()
    
    print("SQLite version: {}".format(data[0]))
    print('------------------------------')
    
    # Setup logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s|%(levelname)s|%(name)s| %(message)s'))
    logger.addHandler(handler)
    
    client.run(sys.argv[1])
