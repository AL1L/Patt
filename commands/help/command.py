async def execute(context):
    msg = context.message
    client = context.client
    with open("C:/Users/Allen/DiscordPyBot/commands/help/help.txt") as f:
        contents = f.read()
        contents = contents.replace('%prefix%', context.client_server_data[1])
        contents = contents.replace('%server_name%', msg.server.name)
        await client.send_message(msg.author, '{}'.format(contents))
        await client.send_message(msg.channel, '<@{}>: I DMed you the help.'.format(msg.author.id))
        
async def help(client, msg):
    with open("C:/Users/Allen/DiscordPyBot/commands/help/help.txt") as f:
        contents = f.read()
        contents = contents.replace('%prefix%', '!')
        contents = contents.replace('%server_name%', 'DEFAULT')
        await client.send_message(msg.author, '{}'.format(contents))
