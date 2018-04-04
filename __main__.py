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
import json

print('Loading assets...')

global patt
patt = None

client = discord.Client()


# When bot is ready
@client.event
async def on_ready():
    if config['logging']['server'] is not None and config['logging']['channel'] is not None:
        patt.log_channel = client.get_guild(config['logging']['server']).get_channel(config['logging']['channel'])
    print('------------------------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------------------')
    # await client.change_presence(game=discord.Game(name='Talk to me!'))
    if patt.log_channel is not None:
        time_took = int(round(time.time() * 1000)) - sk_start_time
        embed = await u.log(patt, {
            'Start Time': u.format_ms_time(sk_start_time),
            'Ready At': u.format_ms_time(sk_start_time + time_took),
            'PID': os.getpid()
        }, title='Bot Started', footer="\U000023F3 Took {}ms".format(time_took))


# When a message is sent that can be read by Patt
@client.event
async def on_message(msg):
    # Start Time
    start_time = int(round(time.time() * 1000))

    # Channel cannot be private
    if client.user.id == msg.author.id or msg.content.startswith('#') or msg.author.bot:
        return
    if '<@{}>'.format(client.user.id) in msg.content or '<@!{}>'.format(client.user.id) in msg.content or isinstance(msg.channel, discord.abc.PrivateChannel) or msg.channel.name == 'patt':
        await msg.channel.trigger_typing()
        importlib.reload(ai)
        await ai.on_message(patt, msg, start_time)
        return
    return


# When Patt joins a Guild
@client.event
async def on_guild_join(svr):
    start_time = int(round(time.time() * 1000))
    cur.execute("INSERT INTO guilds VALUES('{}')".format(svr.id))
    db.commit()
    if patt.log_channel is not None:
        time_took = int(round(time.time() * 1000)) - start_time
        embed = await u.log(patt, {
            'Guild': '`'+svr.name+'` _('+str(svr.id)+')_',
            'Owner': '`'+svr.owner.name+'#'+svr.owner.discriminator+'` _('+str(svr.owner.id)+')_',
            'Users': str(len(svr.members)),
            'Is Large': str(svr.large),
            'Start Time': u.format_ms_time(start_time),
            'End Time': u.format_ms_time(start_time + time_took)
        }, title='Added to Guild', footer="\U000023F3 Took {}ms".format(time_took), thumbnail=svr.icon_url)
    await update_guild_count()


# When Patt leaves a guild
@client.event
async def on_guild_remove(svr):
    start_time = int(round(time.time() * 1000))
    cur.execute("DELETE FROM guilds WHERE gid='{}'".format(svr.id))
    db.commit()
    if patt.log_channel is not None:
        time_took = int(round(time.time() * 1000)) - start_time
        embed = await u.log(patt, {
            'Guild': '`'+svr.name+'` _('+str(svr.id)+')_',
            'Owner': '`'+svr.owner.name+'#'+svr.owner.discriminator+'` _('+str(svr.owner.id)+')_',
            'Users': str(len(svr.members)),
            'Is Large': str(svr.large),
            'Start Time': u.format_ms_time(start_time),
            'End Time': u.format_ms_time(start_time + time_took)
        }, title='Removed from Guild', footer="\U000023F3 Took {}ms".format(time_took), thumbnail=svr.icon_url, color=discord.Colour.red())
    await update_guild_count()
    
async def update_guild_count():
    if patt.dbl_token is None:
        return
    amt = len(patt.client.guilds)
    pl = {'server_count': amt}
    hd = {'Authorization': patt.dbl_token}
    r = await aiohttp.request('POST', 'https://discordbots.org/api/bots/{}/stats'.format(client.user.id), headers=hd, data=pl)
    # print(r)
    return r
    


if __name__ == "__main__":    
    print('------------------------------')
    print('Parameters: {}'.format(sys.argv))
    config = None
    try:
        config = json.load(open('config.json'))
    except Exception as e:
        print('------------------------------')
        print('Missing or invalid config file.')
        print(e)
        quit(1)
    
    if 'discord_token' not in config or \
       'apiai_token' not in config or \
       'dbl_token' not in config or \
       'oxford_dictionaries' not in config or \
       'logging' not in config or \
       'admins' not in config or \
       'database' not in config:
        print('------------------------------')
        print('Invalid config file.')
        quit(1)
    
    if 'server' not in config['logging'] or \
       'channel' not in config['logging']:
        print('------------------------------')
        print('Invalid logging in config file.')
        quit(1)
    
    if 'id' not in config['oxford_dictionaries'] or \
       'key' not in config['oxford_dictionaries']:
        print('------------------------------')
        print('Invalid oxford dictionary app in config file.')
        quit(1)

    if 'type' not in config['database'] or \
       'database' not in config['database'] or \
       'username' not in config['database'] or \
       'password' not in config['database'] or \
       'port' not in config['database'] or \
       'host' not in config['database']:
        print('------------------------------')
        print('Invalid databse in config file.')
        quit(1)
    
    cur = None
    # DB setup
    if config['database']['type'] == 'SQLite':
        db = lite.connect(config['database']['database'])
        cur = db.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
    else:
        print('------------------------------')
        print('Invalid databse type in config file.')
        quit(1)
        
    
    
    data = cur.fetchone()
    
    print("SQLite version: {}".format(data[0]))
    print('------------------------------')
    
    # Setup logging
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s|%(levelname)s|%(name)s| %(message)s'))
    logger.addHandler(handler)
    
    patt = u.Patt(
        discord_token=config['discord_token'],
        apiai_token=config['apiai_token'],
        client=client,
        database=db,
        cursor=cur,
        start_time=sk_start_time,
        config=config,
        dbl_token=config['dbl_token'],
        oxford_dictionaries=config['oxford_dictionaries']
    )
    
    print('Starting Patt...')
    
    patt.run()
