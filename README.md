# 🚀 Telegram to MEGA Uploader Bot

A private Telegram bot that automatically uploads forwarded Telegram media to your personal MEGA account and sends you the MEGA download link.

**Simple workflow:**

1. Forward a media file to your Telegram bot.
2. The bot downloads the file from Telegram.
3. The bot uploads it to your MEGA account.
4. The bot replies with the MEGA share link.

Files are uploaded into the `MEGA Bot` folder in your MEGA account.

---

## ✨ Features

- Automatic Telegram-to-MEGA uploads.
- Uploads files directly to your personal MEGA account.
- Automatically creates the `MEGA Bot` folder if needed.
- Returns a MEGA share link after a successful upload.
- Private bot access restricted to your Telegram user ID.
- MEGA credentials stored as Railway environment variables.
- Persistent storage for MEGA configuration.
- Docker-based deployment on Railway.

---

## 📋 Requirements

Before starting, you need:

- A Telegram account.
- A Telegram bot token from [@BotFather](https://t.me/BotFather).
- Telegram API credentials from [my.telegram.org](https://my.telegram.org).
- Your Telegram numeric user ID.
- A MEGA account.
- A Railway account.
- A GitHub account.

---

# 🚂 Railway Deployment Guide

Follow these steps in order.

## Step 1 — Fork or copy this repository

Open the repository:

**[MegaUploaderBot on GitHub](https://github.com/ZoroStrawHat7/MegaUploaderBot)**

Fork the repository to your GitHub account, or create your own copy.

You can also deploy your existing fork if you already have one.

## Step 2 — Create a Railway project

1. Open [Railway](https://railway.com/).
2. Sign in or create an account.
3. Click **New Project**.
4. Select **Deploy from GitHub Repo**.
5. Connect your GitHub account if requested.
6. Select your MegaUploaderBot repository.
7. Start the deployment.

Railway will use the included Dockerfile to build the application.

**Important:** The first deployment may fail until you configure the required environment variables and persistent volume. That is expected.

## Step 3 — Create a Railway Volume

The bot needs persistent storage for its MEGA configuration.

1. Open your Railway project.
2. Open your bot service.
3. Go to the **Volumes** section.
4. Create a new volume.
5. Set the mount path to:

`/data`

The bot stores its MEGA configuration at:

`/data/mega.ini`

Do not remove this volume after deployment.

## Step 4 — Get Telegram API credentials

Open:

[https://my.telegram.org](https://my.telegram.org)

1. Log in using your Telegram phone number.
2. Open **API development tools**.
3. Create an application if you do not already have one.
4. Copy your API ID and API Hash.

You will need:

- `APP_ID` — Telegram API ID.
- `API_HASH` — Telegram API Hash.

Keep your API Hash private.

## Step 5 — Create your Telegram bot

Open [@BotFather](https://t.me/BotFather).

1. Send `/newbot`.
2. Enter a name for your bot.
3. Choose a unique username ending in `bot`.
4. Copy the bot token.

You will need:

- `BOT_TOKEN` — Your Telegram bot token.

Never share your bot token publicly.

## Step 6 — Get your Telegram user ID

Your bot is private and only the Telegram user ID configured in `AUTH_USERS` is authorized to use it.

You can obtain your numeric Telegram user ID using a trusted Telegram user-ID bot.

You will need:

- `AUTH_USERS` — Your numeric Telegram user ID.

Example:

`AUTH_USERS=123456789`

Use your own ID, not your Telegram username.

## Step 7 — Generate your Telegram STRING_SESSION

The bot requires a Telegram session string.

This is generated using the repository's included `generate_session.py` script.

### On your computer

Install Python 3.10 or newer.

Clone your repository:

```bash
git clone https://github.com/ZoroStrawHat7/MegaUploaderBot.git
cd MegaUploaderBot
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Set your Telegram API credentials.

**Windows PowerShell:**

```powershell
$env:APP_ID="YOUR_APP_ID"
$env:API_HASH="YOUR_API_HASH"
python generate_session.py
```

**Linux / macOS:**

```bash
export APP_ID="YOUR_APP_ID"
export API_HASH="YOUR_API_HASH"
python3 generate_session.py
```

Follow the login prompts:

1. Enter your Telegram phone number.
2. Enter the verification code sent by Telegram.
3. Enter your two-step verification password if requested.

After successful login, the script will print your `STRING_SESSION`.

Copy it and keep it private.

**Security warning:** A session string can provide access to your Telegram account. Never share it with anyone or commit it to GitHub.

## Step 8 — Add Railway environment variables

Open your Railway bot service.

Go to **Variables** and add the following:

| Variable | Value |
|---|---|
| `APP_ID` | Your Telegram API ID |
| `API_HASH` | Your Telegram API Hash |
| `BOT_TOKEN` | Your BotFather token |
| `STRING_SESSION` | Your generated session string |
| `AUTH_USERS` | Your numeric Telegram user ID |
| `MEGA_EMAIL` | Your MEGA account email |
| `MEGA_PASSWORD` | Your MEGA account password |
| `DATA_DIR` | `/data` |
| `DOWNLOAD_LOCATION` | `/tmp/mega-downloads` |

Replace every example with your own credentials.

Do not add quotation marks around the values unless they are actually part of the credential.

**Never publish your environment variables or credentials.**

## Step 9 — Deploy the bot

After adding all variables:

1. Open the Railway deployment section.
2. Trigger a new deployment if one has not started automatically.
3. Wait for the build to finish.
4. Check the deployment logs.
5. Confirm that the application starts without errors.

If the deployment succeeds, your bot is ready for testing.

---

# 📤 How to Use the Bot

1. Open your Telegram bot.
2. Send `/start`.
3. Forward a media file to the bot.
4. Wait for the download and MEGA upload to finish.
5. The bot will reply with the MEGA share link.

Uploaded files are stored in:

`/Root/MEGA Bot/`

inside your MEGA account.

---

# 💾 Storage and File Size

The bot uses two different storage locations:

| Location | Purpose |
|---|---|
| `/data` | Persistent MEGA configuration |
| `/tmp/mega-downloads` | Temporary downloaded media |

Temporary downloaded files may disappear when Railway restarts or redeploys the container.

### Large file requirements

Make sure your Railway service has enough temporary disk space for the entire file.

For a 4 GB file, allow approximately 8–10 GB of available temporary storage for headroom.

Other factors that affect upload size include:

- Telegram client/library support.
- Telegram message and file limitations.
- Railway storage and resource limits.
- MEGA account storage and transfer quota.
- Network stability and upload time.

**Note:** Support for files up to 4 GB must be verified through actual testing. Do not assume every deployment or file type supports this size.

---

# 🔧 Troubleshooting

### 1. Missing environment variable

Example:

```text
Missing required environment variable: BOT_TOKEN
```

**Solution:** Open Railway Variables and check that all required variables are configured correctly.

### 2. Telegram session error

Check that:

- `APP_ID` is correct.
- `API_HASH` is correct.
- `STRING_SESSION` was generated successfully.
- The session string was copied completely.

### 3. MEGA login error

Check that:

- `MEGA_EMAIL` is correct.
- `MEGA_PASSWORD` is correct.
- Your MEGA account is accessible.
- Your account has sufficient transfer quota.

### 4. Upload fails for large files

Check the available temporary disk space and Railway resource limits.

A file must be downloaded before it can be uploaded to MEGA, so sufficient temporary storage is essential.

### 5. Railway deployment fails

Open the Railway deployment logs and look for the first actual Python or Docker error.

Do not treat ordinary BuildKit or container startup warnings as the application failure without checking the final error.

---

# 🔐 Security

Please follow these security rules:

- Never publish your `BOT_TOKEN`.
- Never publish your `API_HASH`.
- Never publish your `STRING_SESSION`.
- Never publish your MEGA email or password.
- Never commit `.env` files or `mega.ini` to GitHub.
- Keep `AUTH_USERS` restricted to your own numeric Telegram user ID.
- Use Railway Variables for all secrets.
- Protect your Telegram and MEGA accounts with appropriate account security settings.

If your session string or bot token is exposed, revoke or regenerate it immediately.

---

# ⚖️ Disclaimer

This project is intended for personal use.

Only upload files that you own or have permission to transfer. Follow Telegram, MEGA, and Railway terms of service.

File-size support, upload speed, and availability depend on the external services, account limits, and deployment resources.

---

## ❤️ Credits

Based on the [Mega.nz-Bot](https://github.com/partiallywritten/Mega.nz-Bot) project, with modifications for private Telegram-to-MEGA uploading and Railway deployment.

**Made for simple, private, and automatic MEGA uploads.**
