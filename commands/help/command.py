import os
import json
from pathlib import Path
import utils as u


async def execute(context: u.CommandContext):
    commands_directory = "C:/Users/Allen/DiscordPyBot/commands/"
    help_list = "Here is the list of commands:\n\n"
    for dir in get_sub_dirs(commands_directory):
        command_config_file = Path("{}{}/cmd.json".format(commands_directory, dir))

        if not command_config_file.is_file():
            continue

        command_config_text = command_config_file.read_text()
        command_config_json = json.loads(command_config_text)

        if command_config_json is None:
            continue

        usage = command_config_json['usage']

        help_list = help_list + "`" + usage + "` - " + command_config_json['description'] + '\n'

    help_list = help_list.format(cmd_prefix=context.client_server_data[1])

    await context.client.send_message(context.message.author, '{}'.format(help_list))
    await context.client.send_message(context.message.channel, '<@{}>: I DMed you the help.'
                                      .format(context.message.author.id))
    return


def get_sub_dirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
