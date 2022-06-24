import os

ignore = [
    "__init__.py",
]

default = [
    com[:-3] for com in os.listdir("./cogs")
    if com.endswith(".py") and com not in ignore
]


__all__ = (
    "default",
)
