#!./bin/python3

import sys

import discord

import bot
import env


def main() -> None:
    match sys.argv:
        case [_]:
            debug = False
        case [_, "--debug"]:
            debug = True
        case _:
            print(f"Usage: {sys.argv[0]} [--debug]", file=sys.stderr)
            sys.exit(1)

    client = bot.EuroBot(
        intents=discord.Intents.all(),
        help_command=None,
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="Help: /help"
        ),
    )

    @client.event
    async def on_ready() -> None:
        client.logger.info(f"“{client.user}” has logged in.")

    env.init()
    client.initLogger(debug)
    client.loadModules()
    client.run(env.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
