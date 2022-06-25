from __future__ import annotations

import asyncio
import datetime
import logging
import os
import sys
from typing import Any

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

import cogs
from utils.logging import setup_logging


load_dotenv()

TOKEN = os.environ['TOKEN']

log = logging.getLogger(__name__)


class AutoShardedBot(commands.AutoShardedBot):
    user: discord.ClientUser
    uptime: datetime.datetime

    def __init__(self, **kwargs):
        super().__init__(
            command_prefix="!",
            strip_after_prefix=True,
            case_insensitive=True,
            intents=discord.Intents.default(),
            chunk_guilds_at_startup=False,
            **kwargs
        )

        self.ready = False

        log.info(
            f"Cluster Starting {kwargs.get('shard_ids', None)}, {kwargs.get('shard_count', 1)}")

    def __repr__(self) -> str:
        return f"<Friday username=\"{self.user.display_name if self.user else None}\" id={self.user.id if self.user else None}>"

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()

        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.team and self.bot_app_info.team.owner_id or self.bot_app_info.owner.id
        self.owner = self.get_user(self.owner_id) or await self.fetch_user(self.owner_id)

        for cog in cogs.default:
            path = "cogs."
            try:
                await self.load_extension(f"{path}{cog}")
            except Exception as e:
                log.error(f"Failed to load extenstion {cog} with \n {e}")

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()

        log.info(f"Logged in as #{self.user}")

    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return

        await self.process_commands(msg)

    async def close(self) -> None:
        await super().close()
        await self.session.close()

    async def start(self, token: str, **kwargs: Any) -> None:
        await super().start(token, reconnect=True)


async def main(bot):
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    print(f"Python version: {sys.version}")

    bot = AutoShardedBot()
    try:
        with setup_logging():
            asyncio.run(main(bot))
    except KeyboardInterrupt:
        asyncio.run(bot.close())
