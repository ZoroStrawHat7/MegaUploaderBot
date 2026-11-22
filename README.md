# Personal MEGA Telegram Uploader

Minimal private bot based on the supplied Mega.nz-Bot (Cypher) source.

Workflow: forward a Telegram media message to the bot → the bot downloads it → uploads it into `/Root/MEGA Bot/` in your MEGA account → replies with the MEGA export link.

No login conversation, MongoDB, buttons, URL downloader, or public-user mode is enabled. MEGA credentials are read only from environment variables and written at startup to a private config file under the persistent data directory.

## Railway deployment

1. Deploy this repository using the included `Dockerfile`.
2. Add a Railway Volume and mount it at `/data`. The MEGA CLI config is stored at `/data/mega.ini` with owner-only permissions.
3. Add these Railway Variables:
   - `APP_ID` — Telegram API ID from https://my.telegram.org
   - `API_HASH` — Telegram API hash from https://my.telegram.org
   - `BOT_TOKEN` — token from @BotFather
   - `STRING_SESSION` — private Telegram user session string
   - `AUTH_USERS` — your numeric Telegram user ID only
   - `MEGA_EMAIL` — your MEGA account email
   - `MEGA_PASSWORD` — your MEGA account password
   - `DATA_DIR=/data`
   - `DOWNLOAD_LOCATION=/tmp/mega-downloads`
4. Deploy. Open your bot, send `/start`, then forward a media file.

## Storage layout

- `/data/mega.ini` — persistent MEGA CLI configuration.
- `/tmp/mega-downloads` — temporary media downloads. These files are not persistent and may be cleared when the Railway container restarts or is redeployed.
- Set `DOWNLOAD_LOCATION` only if you intentionally want a different temporary download path.

## Important limits and testing

- The app uses an MTProto-based Pyrogram-compatible client (Kurigram), not Telegram's HTTP Bot API file-download endpoint.
- Telegram says non-Premium users can download 4 GB files uploaded by Premium users. Actual 4 GB handling still depends on the Telegram client/library layer and the exact file/message type; test with a file larger than 2 GB before relying on it.
- Temporary storage must have enough free space for the entire download. A 4 GB transfer needs more than 4 GB free; allow at least 8–10 GB for headroom. Confirm the available temporary disk space in your Railway service.
- MEGA account storage and transfer quota must be sufficient. MEGA may also impose account-specific transfer limits.
- Railway plan limits, storage pricing and outbound bandwidth are separate from the code. Confirm the service resources in your Railway dashboard.
- This project has not been deployed to your Railway account or tested against your Telegram/MEGA credentials.

## Security

- Keep the repository private if you later add secrets to files; never commit `.env`, `mega.ini`, session files, or real credentials.
- `AUTH_USERS` must contain only your own numeric Telegram user ID.
- Treat `STRING_SESSION`, `API_HASH`, `BOT_TOKEN`, and MEGA credentials as secrets. Add them only in Railway Variables; never paste them into chat or commit them to GitHub.
- Use a unique MEGA password and enable account security features where available.
