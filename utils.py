import json
import discord
import importlib
from pathlib import Path
import datetime


# Intent context class
class IntentContext(object):
    name = ""
    id = ""
    input = ""
    raw_input = ""
    apiai = None
    output = ""
    output_embed = None
    client = None
    message = None
    start_time = 0
    cursor = None


# Intent context class
class Intent(object):
    @staticmethod
    async def handle(context: IntentContext):
        return


def get_intent(name):
    intent_directory = "C:/Users/user1/Patt/intents/{name}/".format(name=name)
    intent_file = Path("{}/intent.py".format(intent_directory))

    if not intent_file.is_file():
        return None

    package = "intents.{}".format(name)
    name = 'intent'
    intent_sk = getattr(__import__(package, fromlist=[name]), name)
    importlib.reload(intent_sk)
    return intent_sk.Intent()



# def has_permission(cmd, msg):
#     command = get_command(cmd)
# 
#     if command.permissions is not None:
#         req_perms = command.permissions
#         user_perms = msg.channel.permissions_for(msg.author)
#         for req_perm in req_perms:
#             if req_perm.startswith('user:'):
#                 if msg.author.id not in req_perm.split(':')[1].split(','):
#                     return [False, 'INVALID_USER']
#             elif req_perm.startswith('guild:'):
#                 if msg.server.id not in req_perm.split(':')[1].split(','):
#                     return [False, 'INVALID_GUILD']
#             elif req_perm.startswith('channel:'):
#                 if msg.channel.id not in req_perm.split(':')[1].split(','):
#                     return [False, 'INVALID_CHANNEL']
#             else:
#                 if not getattr(user_perms, req_perm):
#                     return [False, req_perm.upper()]
#     return [True]


def format_ms_time(ms):
    stamp = int(ms)
    stamp = stamp / 1000
    time = datetime.datetime.fromtimestamp(stamp)
    return time.strftime("%B %d, %Y - %H:%M:%S.%f (UTC)")


def format_ms_time_simple(ms):
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
