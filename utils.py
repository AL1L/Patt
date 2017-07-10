import json
import discord
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
