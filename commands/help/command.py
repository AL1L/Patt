import os
import discord
import utils as u
import time


class Command(u.Command):
    name = "help"
    description = "Shows a list of commands I can do"
    usage = '{cmd_prefix}help [command]'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        if len(context.args) > 0:
            command = u.get_command(context.args[0])
            perms = ''
            for perm in command.permissions:
                perms += ' • {}'.format(perm) + '\n'
            perms = perms[:-2]
            if len(command.permissions) is 0:
                perms = 'None'
            has_perm = u.has_permission(command.name, context.message)
            embed = discord.Embed()
            embed.color = discord.Colour.green()
            if not has_perm[0]:
                embed.color = discord.Colour.orange()
            embed.title = 'Command: {cmd_name}'.format(cmd_name=command.name)
            embed.description = '**Usage:**\n{cmd_usage}\n\n' + \
                                '**Description:**\n{cmd_description}\n\n' + \
                                '**Type:**\n{cmd_type}\n\n' + \
                                '**Required Permissions:**\n{cmd_perms}\n\n' + \
                                '**You Have Permission:**\n{cmd_has_perm}\n\n'
            embed.description = embed.description.format(cmd_usage=command.usage,
                                                         cmd_description=command.description,
                                                         cmd_type=command.type,
                                                         cmd_perms=perms,
                                                         cmd_has_perm=has_perm[0])
            embed.description = embed.description.format(cmd_prefix=context.client_server_data[1])
            embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
            time_took = int(round(time.time() * 1000)) - context.start_time
            embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))
            await context.client.send_message(context.message.channel, '', embed=embed)
        else:
            commands_directory = "C:/Users/user1/DiscordPyBot/commands/"
            help_list = ''
            embed = discord.Embed()
            embed.color = discord.Colour.green()
            embed.title = 'Command List'
            embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)

            for cmd_name in get_sub_dirs(commands_directory):
                if not u.has_permission(cmd_name, context.message)[0]:
                    continue
                command = u.get_command(cmd_name)

                if command.type == 'hidden':
                    continue

                usage = command.usage.format(cmd_prefix=context.client_server_data[1])

                help_list = help_list + "**" + usage + "**\n" + command.description + '\n\n'

            help_list + help_list[:-2] + '{}'.format(help_list)
            embed.description = help_list
            time_took = int(round(time.time() * 1000)) - context.start_time
            embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))
            await context.client.send_message(context.message.channel, '<@{}> the command list was sent to you.'
                                              .format(context.message.author.id))
            await context.client.send_message(context.message.author, '', embed=embed)


def get_sub_dirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]
