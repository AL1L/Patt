import json
import discord
import importlib
from pathlib import Path


# Command context class
class CommandContext(object):
    name = ""
    message = None
    start_time = 0
    args = []
    database = None
    cursor = None
    client_server_data = []
    client = None


# Command context class
class Command(object):
    name = ""
    usage = "{cmd_prefix}" + name
    description = ""
    type = "none"
    permissions = ['send_messages', 'read_messages']

    @staticmethod
    async def execute(context: CommandContext):
        return


def get_command(name):
    command_directory = "C:/Users/user1/DiscordPyBot/commands/{name}/".format(name=name)
    command_file = Path("{}/command.py".format(command_directory))

    if not command_file.is_file():
        return None

    package = "commands.{}".format(name)
    name = 'command'
    command_sk = getattr(__import__(package, fromlist=[name]), name)
    importlib.reload(command_sk)
    return command_sk.Command()


def get_user_lang(user):
    return "default"


def lang(command, user):
    commands_directory = "C:/Users/user1/DiscordPyBot/commands/"
    if command is '':
        commands_directory = "C:/Users/user1/DiscordPyBot"
    user_lang = get_user_lang(user)
    command_config_file = Path("{}{}/lang.json".format(commands_directory, command))

    if not command_config_file.is_file():
        return None

    command_config_text = command_config_file.read_text()
    command_config_json = json.loads(command_config_text)

    if command_config_json is None:
        return None

    lang_keys = command_config_json[user_lang]

    if lang_keys is None:
        return command_config_json['default']

    return lang_keys


def has_permission(command, msg):
    commands_directory = "C:/Users/user1/DiscordPyBot/commands/"

    command_config_file = Path("{}{}/cmd.json".format(commands_directory, command))

    if not command_config_file.is_file():
        return [True]

    command_config_text = command_config_file.read_text()
    command_config_json = json.loads(command_config_text)

    if command_config_json['permissions'] is not None:
        req_perms = command_config_json['permissions']
        user_perms = msg.channel.permissions_for(msg.author)
        for req_perm in command_config_json['permissions']:
            if req_perm.startswith('user:'):
                if msg.author.id not in req_perm.split(':')[1]:
                    return [False, 'specific_user'.upper()]
            else:
                if not getattr(user_perms, req_perm):
                    return [False, req_perm.upper()]
    return [True]
