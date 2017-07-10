import re
import discord

async def execute(context):
    msg = context.message
    client = context.client
    if msg.author.voice.voice_channel is None:
        await client.send_message(msg.channel, '<@{}>: You are not in a voice channel!'.format(msg.author.id))
        return
    if msg.author.voice.voice_channel.type is not discord.ChannelType.voice:
        await client.send_message(msg.channel, '<@{}>: You are not in a voice channel!'.format(msg.author.id))
        return
    if msg.author.voice.is_afk:
        await client.send_message(msg.channel, '<@{}>: You are not in a voice channel!'.format(msg.author.id))
        return
    pattern = re.compile("^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$")
    if context.args[1] is None:
        await client.send_message(msg.channel, '<@{}>: You must specify a YouTube URL!'.format(msg.author.id))
        return
    if not pattern.match(context.args[1]):
        await client.send_message(msg.channel, '<@{}>: That is not a YouTube URL!'.format(msg.author.id))
        return
    voice_channel = msg.author.voice.voice_channel
    for voice in client.voice_clients:
        voice.disconnect()
    voice = await client.join_voice_channel(voice_channel)
    player = await voice.create_ytdl_player(context.args[1])
    player.start()

# !yt https://www.youtube.com/watch?v=uq7OAmzmGxo