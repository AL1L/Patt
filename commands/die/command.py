import utils as u
import random

class Command(u.Command):
    name = "die"
    description = "Rolls a 6 sided die"
    usage = '{cmd_prefix}die [sides=6]'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        sides = 6
        if len(context.args) >= 2:
            if context.args[0] is not None:
                if context.args[0].isdigit():
                    sides = int(context.args[0])
        
        die = random.randint(1,sides)
        await context.client.send_message(context.message.channel, '<@{}>: I rolled a `{}`'.format(context.message.author.id, die))
