import discord
from discord.ext import commands
from typing import Dict

# from functools import partial
from time import time
import datetime

# import asyncio
from replit import db

homies_stats = {
    "629243339379834880": "1039536960441684101",
    "497352662451224578": "1039536961918079087",
    "737157112026759218": "1039536961918079087",
}


class VC(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._setup = False

    # Convert seconds into hours, minutes and seconds
    @staticmethod
    def convert(seconds):
        return str(datetime.timedelta(seconds=seconds))

    async def setup(self, ctx: commands.Context):
        if self._setup:
            return
        self._setup = True
        self.total_time: Dict[str, int] = {}
        self.current_time: Dict[str, int] = {}
        for homie, stat_message_link in homies_stats.items():

            # Convert message link into message
            stat_message = await commands.MessageConverter().convert(ctx, homies_stats[homie])

            # Filter out time (in seconds) from message
            total_time = int(stat_message.clean_content.split("\n")[0].split("-")[1].strip())

            self.total_time[homie] = total_time

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):

        if not (str(member.id) in homies_stats.keys()):
            return
        # #just in case
        # time.sleep(5)

        # Once a user joins the vc
        if before.channel is None and after.channel.id == 1030713824615084052:
            db[str(member.id) + "c"] = int(time())

        # Once a user leaves the vc
        elif after.channel is None and before.channel.id == 1030713824615084052:
            elapsed_time = int(time()) - db[str(member.id) + "c"]
            db[str(member.id) + "t"] += elapsed_time

            # Convert message link into message
            channel = member.dm_channel or await member.create_dm()
            stat_message = await channel.fetch_message(homies_stats[str(member.id)])

            await stat_message.edit(
                content=f"Total time: {self.convert(db[str(member.id) + 't'])}\nLast recorded time: {self.convert(elapsed_time)}"
            )
            if member.id == 497352662451224578:
                await channel.send(
                    content=f"Total time: {self.convert(db[str(member.id) + 't'])}\nLast recorded time: {self.convert(elapsed_time)}"
                )


async def setup(bot: commands.Bot):
    await bot.add_cog(VC(bot))
