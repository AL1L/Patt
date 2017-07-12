import utils as u
import random

class Command(u.Command):
    name = "dice"
    description = "Rolls two 6 sided dice"
    usage = '{cmd_prefix}dice'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        await context.client.send_message(context.message.channel, '<@{}>: I rolled a `{}` and a `{}` with a total of `{}`'.format(context.message.author.id, die1, die2, (die1+die2)))
