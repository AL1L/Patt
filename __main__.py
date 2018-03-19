import time

sk_start_time = int(round(time.time() * 1000))

import discord
import utils as u
import logging
import sys
import os
import traceback
import sqlite3 as lite
import importlib
import ai
import aiohttp
print('Starting...')
global log_channel
os.system('cls')

if __name__ == "__main__":
    # Create Discord client
    client = discord.Client()


# When bot is ready
@client.event
async def on_ready():
    global log_channel
    log_channel = client.get_server("366785187029188609").get_channel('366785269351055360')
    print('------------------------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------------------')
    await client.change_presence(game=discord.Game(name='Talk to me!'))
    time_took = int(round(time.time() * 1000)) - sk_start_time
    embed = discord.Embed()
    embed.description = '**Start Time:**\n{start}\n\n' + \
                        '**Ready At:**\n{end}\n\n' + \
                        '**PID:**\n{pid}\n\n'
    embed.description = embed.description.format(start=u.format_ms_time(sk_start_time),
                                                 end=u.format_ms_time(sk_start_time + time_took),
                                                 pid=os.getpid())
    embed.title = 'Bot Started'
    embed.color = discord.Colour.green()
    embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
    await client.send_message(log_channel, '', embed=embed)


# When a message is sent that can be read by Patt
@client.event
async def on_message(msg):
    # Start Time
    start_time = int(round(time.time() * 1000))

    # Channel cannot be private
    if client.user.id == msg.author.id:
        return
    if '<@{}>'.format(client.user.id) in msg.content or msg.channel.is_private:
        await client.send_typing(msg.channel)
        importlib.reload(ai)
        await ai.on_message(client, cur, msg, start_time)
        return
    return


# When Patt joins a server
@client.event
async def on_server_join(svr):
    start_time = int(round(time.time() * 1000))
    cur.execute("INSERT INTO guilds VALUES('{}', 'p!')".format(svr.id))
    db.commit()
    time_took = int(round(time.time() * 1000)) - start_time
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
    await update_server_count()


# When Patt leaves a server
@client.event
async def on_server_remove(svr):
    start_time = int(round(time.time() * 1000))
    cur.execute("DELETE FROM guilds WHERE gid='{}'".format(svr.id))
    db.commit()
    time_took = int(round(time.time() * 1000)) - start_time
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
    await update_server_count()
    
async def update_server_count():
    cur.execute("SELECT * FROM guilds")
    rows = cur.fetchall()
    amt = len(rows)
    pl = {'server_count': amt}
    hd = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM5NTMzNjIxODMxODk5NTQ1NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNTIxMzQyMDc0fQ.e7l7wjucJPpkIvUA4Gyzt2KKJ5NGirnuRg6VT229Ngw'}
    r = await aiohttp.request('POST', 'https://discordbots.org/api/bots/395336218318995457/stats', headers=hd, data=pl)
    # print(r)
    return r
    


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
