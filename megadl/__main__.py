import asyncio
import os

from pyrogram import Client, idle

from . import CypherClient


async def main():
    user_client = Client(
        "MegaBotUserSession",
        api_id=int(os.environ["APP_ID"]),
        api_hash=os.environ["API_HASH"],
        session_string=os.environ["STRING_SESSION"],
        in_memory=True,
    )

    await user_client.start()
    CypherClient.user_client = user_client
    CypherClient.bot_id = int(os.environ["BOT_TOKEN"].split(":", 1)[0])
    await CypherClient.start()
    print("MEGA uploader is online")

    try:
        await idle()
    finally:
        await CypherClient.stop()
        await user_client.stop()


if __name__ == "__main__":
    asyncio.run(main())
