import os
import sys
from pathlib import Path


def required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    if "\n" in value or "\r" in value:
        raise SystemExit(f"Invalid newline in environment variable: {name}")
    return value


def main() -> None:
    required("APP_ID")
    required("API_HASH")
    required("BOT_TOKEN")
    required("STRING_SESSION")
    required("MEGA_EMAIL")
    required("MEGA_PASSWORD")
    allowed = required("AUTH_USERS")
    if not allowed.isdigit():
        raise SystemExit("AUTH_USERS must be your numeric Telegram user ID (one ID only).")

    data_dir = Path(os.getenv("DATA_DIR", "/data"))
    download_dir = data_dir / "downloads"
    download_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    cfg_path = data_dir / "mega.ini"
    config_text = (
        "[Login]\n"
        f"Username = {os.environ['MEGA_EMAIL']}\n"
        f"Password = {os.environ['MEGA_PASSWORD']}\n\n"
        "[Network]\n"
        "SpeedLimit = 0\n"
        "ParallelTransfers = 4\n"
    )
    cfg_path.write_text(config_text, encoding="utf-8")
    os.chmod(cfg_path, 0o600)

    os.environ["MEGA_CONFIG_PATH"] = str(cfg_path)
    os.environ["DOWNLOAD_LOCATION"] = str(download_dir)
    os.environ["USE_ENV"] = "False"

    os.execv(sys.executable, [sys.executable, "-m", "megadl"])


if __name__ == "__main__":
    main()
