import json
import discord
import importlib
from pathlib import Path
import datetime

class Patt(object):
    client = None
    database = None
    cursor = None
    start_time = 0
    log_channel = None
    apiai_token = None
    discord_token = None
    dbl_token = None,
    config = {},
    oxford_dictionaries = {}
    
    
    def __init__(self, discord_token=None, apiai_token=None, client=None, database=None, cursor=None, start_time=0, log_channel=None, dbl_token=None, config={}, oxford_dictionaries={}):
        self.client = client
        self.database = database
        self.cursor = cursor
        self.start_time = start_time
        self.log_channel = log_channel
        self.apiai_token = apiai_token
        self.discord_token = discord_token
        self.dbl_token = dbl_token
        self.config = config
        self.oxford_dictionaries = oxford_dictionaries
    
    def run(self):
        self.client.run(self.discord_token)
        
# Intent context class
class IntentContext(object):
    name = ""
    id = ""
    input = ""
    raw_input = ""
    apiai = None
    output = ""
    output_embed = None
    message = None
    start_time = 0
    request = None
    user = None
    patt = None
    
class User(object):
    discard_user = None
    id = 0
    age = None
    nsfw_enabled = False
    language = 'en'
    nickname = None

async def log(patt: Patt, f: dict, inline=True, footer=None, title=None, color=None, send=True, image=None, thumbnail=None):
    embed: discord.Embed = discord.Embed()
    for k,v in f.items():
        if v is not None:
            embed.add_field(name=str(k), value=str(v), inline=inline)
    if footer is not None:
        embed.set_footer(text=footer)
    if title is not None:
        embed.title = title
    if image is not None:
        embed.set_image(url=image)
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)

    if color is None:
        color = discord.Colour.green()

    embed.color = color

    if send: 
        await patt.log_channel.send('', embed=embed)
    return embed
    
    
    
    
def get_user(patt: Patt, id: int):
    user = User()
    user.discard_user = patt.client.get_user(id)
    user.id = int(id)
    patt.cursor.execute("SELECT * FROM users WHERE id='{}'".format(user.id))
    data = patt.cursor.fetchone()
    if data is not None:
        if data[1] is not None:
            user.age = int(data[1])
            user.nsfw_enabled = user.age >= 18
        user.language = data[2]
        user.nickname = data[3]
    else:
        patt.cursor.execute("INSERT INTO users VALUES('{}', NULL, 'en', NULL)".format(user.id))
        patt.database.commit()
        

# Intent context class
class Intent(object):
    @staticmethod
    async def handle(context: IntentContext):
        return


def get_intent(name: str):
    intent_directory = "intents/{name}/".format(name=name)
    intent_file = Path("{}/intent.py".format(intent_directory)) 
    
    if not intent_file.is_file():
        return None

    package = "intents.{}".format(name)
    name = 'intent'
    intent_sk = getattr(__import__(package, fromlist=[name]), name)
    importlib.reload(intent_sk)
    return intent_sk.Intent()


def format_ms_time(ms: int):
    stamp = int(ms)
    stamp = stamp / 1000
    time = datetime.datetime.fromtimestamp(stamp)
    return time.strftime("%B %d, %Y - %H:%M:%S.%f (UTC)")


def format_ms_time_simple(ms:int):
    stamp = int(ms)
    stamp = stamp / 1000
    time = datetime.datetime.fromtimestamp(stamp)
    return time.strftime("%B %d, %Y - %I:%M %p")
    
def get_hex_color(dColor: discord.Colour):
    r = hex(dColor.r)[2:]
    g = hex(dColor.g)[2:]
    b = hex(dColor.b)[2:]
    color = '{}{}{}'.format(r,g,b)
    return color
