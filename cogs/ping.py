from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands
from utils.time import human_timedelta

if TYPE_CHECKING:
    from index import AutoShardedBot


class Ping(commands.Cog):
    """Ping? Pong!"""

    def __init__(self, bot: AutoShardedBot):
        self.bot: AutoShardedBot = bot

    def __repr__(self) -> str:
        return f"<cogs.{self.__cog_name__} content=\"Pong\">"

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Pong!"""
        shard = ctx.guild and self.bot.get_shard(ctx.guild.shard_id)
        latency = f"{shard.latency*1000:,.0f}" if shard is not None else f"{self.bot.latency*1000:,.0f}"
        await ctx.send(f"Ping!\n⏳ API is {latency}ms")

    def get_bot_uptime(self, *, brief: bool = False) -> str:
        return human_timedelta(self.bot.uptime, accuracy=None, brief=brief, suffix=False)

    @commands.hybrid_command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        """Uptime!"""
        await ctx.send(f"Uptime: **{self.get_bot_uptime}**")


async def setup(bot: AutoShardedBot):
    await bot.add_cog(Ping(bot))
