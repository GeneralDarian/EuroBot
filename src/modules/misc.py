import logging

from bot import EuroBot

logger = logging.getLogger(f"{EuroBot.name}.{__name__}")


def init(client):
    @client.tree.command(name="ping", description="Ping the bot")
    async def ping(interaction):
        logger.debug("Bot pinged!")
        await client.send(interaction, f"Pong! {round(client.latency * 1000)}ms")
