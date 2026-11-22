import os
import time
import logging

from pyrogram import filters
from pyrogram.types import Message

from megadl import CypherClient
from megadl.lib.megatools import MegaTools
from megadl.helpers.pyros import track_progress


MEDIA_FILTER = (
    filters.document
    | filters.photo
    | filters.video
    | filters.animation
    | filters.audio
    | filters.voice
    | filters.video_note
)


@CypherClient.on_message(filters.private & MEDIA_FILTER)
@CypherClient.run_checks
async def up_to(client: CypherClient, msg: Message):
    user_id = msg.from_user.id if msg.from_user else msg.chat.id
    if user_id in client.uploading_users:
        return await msg.reply_text("A file is already being uploaded. Please wait for it to finish.")

    client.uploading_users.add(user_id)
    user_dir = os.path.join(client.dl_loc, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    status = await msg.reply_text("📥 Downloading your media from Telegram…")
    local_path = None

    try:
        started = time.time()
        # Retrieve the same private-chat message from the owner's logged-in
        # MTProto user session. This avoids the HTTP Bot API's 20 MB download cap
        # and lets the personal account download files up to Telegram's 4 GB limit.
        source_message = await client.user_client.get_messages(
            client.bot_id, msg.id
        )
        if not source_message or not source_message.media:
            raise RuntimeError("Could not retrieve the forwarded media with the owner session.")

        local_path = await client.user_client.download_media(
            source_message,
            file_name=f"{user_dir}/",
            progress=track_progress,
            progress_args=(client, msg.chat.id, status.id, started),
        )
        if not local_path or not os.path.isfile(local_path):
            raise RuntimeError("Telegram did not return a downloaded file.")

        await status.edit_text("☁️ Download complete. Uploading to your MEGA `MEGA Bot` folder…")
        mega = MegaTools(client)
        link = await mega.upload(
            local_path,
            user_id,
            msg.chat.id,
            status.id,
            to_path="MEGA Bot",
        )
        await status.edit_text(
            f"✅ Uploaded to MEGA Bot\n\nMEGA link: {link}"
        )
    except Exception as exc:
        logging.exception("MEGA media transfer failed")
        try:
            await status.edit_text(f"❌ Upload failed: `{str(exc)[:700]}`")
        except Exception:
            pass
    finally:
        client.uploading_users.discard(user_id)
        await client.full_cleanup(user_dir, user_id)
