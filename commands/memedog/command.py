import utils as u


class Command(u.Command):
    name = "memedog"
    description = "This is an easteregg MeMeDoG"
    usage = '{cmd_prefix}memedog'
    type = "hidden"

    @staticmethod
    async def execute(context: u.CommandContext):
        msg = context.message
        client = context.client
        memedog = "╭━━━━╮ \n╰┃ ┣▇━▇       This is memedog.\n ┃ ┃  ╰━▅╮ \n ╰┳╯ ╰━━┳╯  \n  ╰╮ ┳━━╯ \n ▕▔▋ ╰╮╭━╮ \n╱▔╲▋╰━┻┻╮╲╱▔▔▔╲\n▏  ▔▔▔▔▔▔▔  O O┃ \n╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱\n ▏╳▕▇▇▕ ▏╳▕▇▇▕\n ╲▂╱╲▂╱ ╲▂╱╲▂╱"
        await client.send_message(msg.channel, memedog)
