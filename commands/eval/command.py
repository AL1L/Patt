import discord
import time
import utils as u


class Command(u.Command):
    name = "eval"
    description = "Do some maths"
    usage = '{cmd_prefix}eval'
    type = "none"

    @staticmethod
    async def execute(context: u.CommandContext):
        embed = discord.Embed()
        embed.title = "Evaluate"
        embed.color = discord.Colour.green()
        evaluate = ""
        for str in context.args:
            evaluate = evaluate + str + " "
        if evaluate is "":
            evaluate = "\"\""
        evaluateOrg = evaluate
        if "stop()" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (stop())\""
        elif "shutdown" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (shutdown)\""
        elif "rundll32.exe" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (rundll32.exe)\""
        elif "import os" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (import os)\""
        elif "os.system" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (os.system)\""
        elif "subprocess.call" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (subprocess.call)\""
        elif "webbrowser" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (webbrowser)\""
        elif "exec" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (exec())\""
        elif "eval" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (eval())\""
        elif "context.database" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (context.database)\""
        elif "context.cursor" in evaluate.lower():
            embed.color = discord.Colour.orange()
            evaluate = "\"That is not allowed! (context.cursor)\""

        if "217617036749176833--" in context.message.author.id:  # DotRar#6028
            embed.color = discord.Colour.dark_red()
            evaluate = "\"You are banned form using this command\""
        elif "146096009246670859--" in context.message.author.id:  # Joey#3518
            embed.color = discord.Colour.dark_red()
            evaluate = "\"You are banned form using this command\""

        try:
            evaluation = eval(evaluate)
        except Exception as e:
            evaluation = e
            embed.color = discord.Colour.red()
        embed.description = "\n`{}` = \n```\n{}\n```\n".format(evaluateOrg, evaluation)
        embed.set_author(name=context.message.author.name, icon_url=context.message.author.avatar_url)
        time_took = int(round(time.time() * 1000)) - context.start_time
        embed.set_footer(text="\U000023F3 Took {}ms".format(time_took))
        await context.client.send_message(context.message.channel, '', embed=embed)
