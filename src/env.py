import os

import dotenv


def init():
    dotenv.load_dotenv()
    env_vars = {}
    for x in [
        "DISCORD_TOKEN",
        "FOTW_CHANNEL_ID",
        "FOTW_EMOTE_ID",
        "FOTW_EMOTE_NAME",
        "GUILD_ID",
        "HELP_EMOTE_ID",
        "VERIFIED_TRADER_GROUP_ID",
    ]:
        if (v := os.getenv(x)) is None:
            raise EnvironmentError(f"Environment Variable '{x}' is not set")
        globals()[x] = v
