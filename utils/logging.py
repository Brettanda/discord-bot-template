from __future__ import annotations

import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler

from discord.client import _ColourFormatter

try:
    import uvloop  # type: ignore
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class _ColourFormatterFile(_ColourFormatter):
    @property
    def FORMATS(self):
        return{
            level: logging.Formatter(
                '{asctime} {levelname:<8} {name:<16} {message}',
                '%Y-%m-%d %H:%M:%S',
                style="{"
            )
            for level, colour in self.LEVEL_COLOURS
        }


class RemoveDuplicate(logging.Filter):
    def __init__(self):
        super().__init__(name='discord')

    def filter(self, record):
        if "discord" in record.name:
            return False
        return True


class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name='discord.state')

    def filter(self, record):
        if record.levelname == 'WARNING' and 'referencing an unknown' in record.msg:
            return False
        return True


class setup_logging:
    """Setup logging for the bot.

      Example Usage: ::
        with setup_logging():
          asyncio.run(bot())
    """

    def __init__(self) -> None:
        self.log = logging.getLogger()

    def __enter__(self) -> None:
        max_bytes = 8 * 1024 * 1024  # 8 MiB to fit in a discord message
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.getLogger('discord.state').addFilter(RemoveNoise())

        self.log.setLevel(logging.INFO)

        filehandler = RotatingFileHandler(filename="logging.log", encoding="utf-8", mode="w", maxBytes=max_bytes, backupCount=5)
        filehandler.setFormatter(_ColourFormatterFile())

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_ColourFormatter())
        handler.addFilter(RemoveDuplicate())

        self.log.addHandler(filehandler)
        self.log.addHandler(handler)

    def __exit__(self) -> None:
        handlers = self.log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            self.log.removeHandler(hdlr)
