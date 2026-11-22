# Personal MEGA Telegram Uploader

Minimal private bot based on the supplied Mega.nz-Bot (Cypher) source.

**Workflow:** forward a Telegram media message to the bot → the bot downloads it → uploads it into `/Root/MEGA Bot/` in your MEGA account → replies with the MEGA export link.

No login conversation, MongoDB, buttons, URL downloader, or public-user mode is enabled. MEGA credentials are read only from environment variables and written at startup to a private config file under the persistent data directory.

## Railway deployment

1. Create a new Railway project and deploy this folder/repository using the included `Dockerfile`.
2. Add a Railway Volume and mount it at `/data`. Large files are downloaded to `/data/downloads`; the MEGA CLI config is stored at `/data/mega.ini` with owner-only permissions.
3. Add these Railway Variables:
   - `APP_ID` — Telegram API ID from https://my.telegram.org
   - `API_HASH` — Telegram API hash from https://my.telegram.org
   - `BOT_TOKEN` — token from @BotFather
   - `AUTH_USERS` — your numeric Telegram user ID only
   - `MEGA_EMAIL` — your MEGA account email
   - `MEGA_PASSWORD` — your MEGA account password
   - `DATA_DIR=/data`
4. Deploy. Open your bot, send `/start`, then forward a media file.

## Important limits and testing

- The app uses an MTProto-based Pyrogram-compatible client (Kurigram), not Telegram's HTTP Bot API file-download endpoint.
- Telegram says non-Premium users can download 4 GB files uploaded by Premium users. Actual 4 GB handling still depends on the Telegram client/library layer and the exact file/message type; test with a file larger than 2 GB before relying on it.
- A Railway Volume must have enough free space for the entire temporary download. A 4 GB transfer needs more than 4 GB free; allow at least 8–10 GB for headroom. The volume is not automatically expanded by this project.
- MEGA account storage and transfer quota must be sufficient. MEGA may also impose account-specific transfer limits.
- Railway plan limits, storage pricing and outbound bandwidth are separate from the code. Confirm the volume and service resources in your Railway dashboard.
- This project has not been deployed to your Railway account or tested against your Telegram/MEGA credentials. The ZIP is prepared, not live-verified.

## Security

- Keep the repository private if you later add secrets to files; never commit `.env`, `mega.ini`, session files, or real credentials.
- `AUTH_USERS` must contain only your own numeric Telegram user ID.
- Use a unique MEGA password and enable account security features where available.
