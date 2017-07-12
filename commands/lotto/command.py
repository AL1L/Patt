import utils as u
import random
import time
import discord
import asyncio

class Command(u.Command):
    name = "lotto"
    description = "Ever wanted to win the lotto? Well too bad!"
    usage = '{cmd_prefix}lotto'
    type = "none"
    
    @staticmethod
    async def execute(context: u.CommandContext):
        images = ['\U0001F345', '\U0001F346', '\U0001F347', '\U0001F348', '\U0001F349', '\U0001F34A', '\U0001F34C', 
                    '\U0001F34D', '\U0001F34E', '\U0001F34F', '\U0001F351', '\U0001F352', '\U0001F353']
        
        instant_win = (random.randint(1, 100) > 75)
        
        slot1 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
        slot2 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
        slot3 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
        
        message = '```\n  ' + slot1[0] + slot2[0] + slot3[0] + '  \n->' + slot1[1] + slot2[1] + slot3[1] + '<-\n  ' + slot1[2] + slot2[2] + slot3[2] + '  \n```'
        
        time_took = int(round(time.time() * 1000)) - context.start_time
        
        embed = discord.Embed()
        embed.color = discord.Colour.gold()
        embed.description = message
        embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
        embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))
        
        slots = await context.client.send_message(context.message.channel, '', embed=embed)
        
        slot1 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
        slot2 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
        slot3 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
        
        timer = 0
        
        while timer < 4:
            await asyncio.sleep(0.2)
            timer += 1
        
            slot1 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
            slot2 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
            slot3 = [images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)], images[random.randint(0, len(images)-1)]]
            
            message = '```\n  ' + slot1[0] + slot2[0] + slot3[0] + '  \n->' + slot1[1] + slot2[1] + slot3[1] + '<-\n  ' + slot1[2] + slot2[2] + slot3[2] + '  \n```'
            
            time_took = int(round(time.time() * 1000)) - context.start_time
            
            embed.description = message
            embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))
            slots = await context.client.edit_message(slots, '', embed=embed)
        
        if instant_win:
            slot2[1] = slot1[1]
            slot3[1] = slot1[1]
        
        win = (slot1[1] is slot2[1] and slot1[1] is slot3[1])
        
        message = '```\n  ' + slot1[0] + slot2[0] + slot3[0] + '  \n->' + slot1[1] + slot2[1] + slot3[1] + '<-\n  ' + slot1[2] + slot2[2] + slot3[2] + '  \n```'
        
        if win:
            title = "Congratz! You won! Here is your prize: " + slot1[1]
            embed.color = discord.Colour.green()
        else:
            title = "Sorry, you didn't win this time."
            embed.color = discord.Colour.red()
        
        time_took = int(round(time.time() * 1000)) - context.start_time
        
        embed.title = title
        embed.description = message
        embed.set_footer(text="\U000023F3 Took {time}ms".format(time=time_took))
        
        slots = await context.client.edit_message(slots, '', embed=embed)
    