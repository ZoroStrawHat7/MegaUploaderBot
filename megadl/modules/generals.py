from pyrogram import filters
from pyrogram.types import Message

from megadl import CypherClient


@CypherClient.on_message(filters.command("start") & filters.private)
@CypherClient.run_checks
async def start_msg(_: CypherClient, msg: Message):
    await msg.reply_text(
        "Send or forward a Telegram video, document, audio or photo here. "
        "I'll upload it to your MEGA account in the `MEGA Bot` folder and return the link."
    )


@CypherClient.on_message(filters.command("help") & filters.private)
@CypherClient.run_checks
async def help_msg(_: CypherClient, msg: Message):
    await msg.reply_text(
        "Forward media to this private chat. The bot downloads it, uploads it to "
        "your MEGA `MEGA Bot` folder, then replies with the MEGA link."
    )
