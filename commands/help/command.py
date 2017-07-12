import os
import json
from pathlib import Path
import utils as u


class Command(u.Command):
    name = "help"
    description = "Shows a list of commands I can do"
    usage = '{cmd_prefix}help'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        commands_directory = "C:/Users/user1/DiscordPyBot/commands/"
        help_list = "Here is the list of commands:\n\n```"
        max_len = 0
        for dir in get_sub_dirs(commands_directory):
            command = u.get_command(dir)
                
            if command.type == 'hidden':
                continue
    
            usage = command.usage.format(cmd_prefix=context.client_server_data[1])
            if len(usage) > max_len:
                max_len = len(usage)
                
        for dir in get_sub_dirs(commands_directory):
            command = u.get_command(dir)
                
            if command.type == 'hidden':
                continue
    
            usage = command.usage.format(cmd_prefix=context.client_server_data[1])
    
            spaces = ' ' * (max_len-len(usage))
            help_list = help_list + "" + usage + spaces + " - " + command.description + '\n'
    
        help_list = help_list
    
        await context.client.send_message(context.message.author, '{}```'.format(help_list))
        await context.client.send_message(context.message.channel, '<@{}>: I DMed you the help.'
                                        .format(context.message.author.id))
        return


def get_sub_dirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]