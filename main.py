import os
import discord
from io import StringIO
from contextlib import redirect_stdout
from discord.ext.commands import Bot
import logging
import time
from traceback import format_exc
import requests
from textwrap import indent
import keep_alive


class bottttt(Bot):
    def __init__(self):
        super().__init__(command_prefix="h", intents=discord.Intents.all())

    async def setup_hook(self):
        await self.load_extension("Cogs.VC")

    async def on_ready(self):
        print("Ready!")


client = bottttt()
times = {}


def cleanup_code(content: str) -> str:
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    content = content.replace("```", "\n```")
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])

    return content.strip("` \n")


# backup, and for reference

# @client.event
# async def on_voice_state_update(member, before, after):
#     # print(after.channel.id)
#     # print(before.channel.id)
#     try:
#         if after.channel.id == 1030713824615084052:
#             # try:
#                 print(f'{member} has joined the vc')
#                 times[member.id] = time.time()
#             # except: pass
#     except: pass

#     try:
#         if before.channel.id == 1030713824615084052:
#         # try:
#             print(f'{member} has left the vc')
#             times[member.id] = time.time()-times[member.id]
#             await member.send(f'You have been in the vc for {times[member.id]}')
#     except: pass


@client.command()
async def eval(ctx, *, body):
    env = {"Client": client, "ctx": ctx, "channel": ctx.channel, "author": ctx.author, "guild": ctx.guild, "message": ctx.message}

    env.update(globals())

    body = cleanup_code(body)
    stdout = StringIO()

    to_compile = f'async def func():\n{indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

    func = env["func"]
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f"```py\n{value}{format_exc()}\n```")
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction("\u2705")
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f"```py\n{value}\n```")
        else:
            await ctx.send(f"```py\n{value}{ret}\n```")


TOKEN = os.environ["TOKEN"]
# TOKEN = os.environ['TOKEN']
keep_alive.keep_alive()
r = requests.head(url="https://discord.com/api/v1")
try:
    try:
      print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
    except: pass

except:
    print("No rate limit")
    client.run(TOKEN)
client.run(TOKEN)
