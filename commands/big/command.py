import utils as u


class Command(u.Command):
    name = "big"
    description = "Turns your text big!"
    usage = '{cmd_prefix}big <message>'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        message = ""
        for arg in context.args:
            message = message + arg.upper() + " "

        bgs = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 \U0001F51F 1\U000020E3 2\U000020E3 3\U000020E3 ' \
              '4\U000020E3 5\U000020E3 6\U000020E3 7\U000020E3 8\U000020E3 9\U000020E3 0\U000020E3'.split(' ')
        sms = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 10 1 2 3 4 5 6 7 8 9 0'.split(' ')

        chars = list(message)

        new_message = ''

        for char in chars:
            if char not in sms:
                new_message = "{0}{1}".format(new_message, char) + '\n'
                continue
            new_message = "{0}{1}".format(new_message, bgs[sms.index(char)]) + '\n'

        new_message = new_message[:-2]
        new_message = new_message.replace(' ', '<:blank:334159727036727297>')
        new_message = new_message.replace('\n', ' ')

        await context.client.send_message(context.message.channel, new_message)
