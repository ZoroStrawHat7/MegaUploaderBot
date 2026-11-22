import asyncio
import os

from pyrogram import Client


async def main():
    api_id = int(os.environ["APP_ID"])
    api_hash = os.environ["API_HASH"]

    async with Client(
        "mega_session_generator",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    ) as app:
        print("\nYour Telegram session string (keep it secret):\n")
        print(await app.export_session_string())
        print("\nAdd this value to Railway as STRING_SESSION. Do not share it.\n")


if __name__ == "__main__":
    asyncio.run(main())
