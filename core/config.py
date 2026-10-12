import configparser
import os
from pathlib import Path


def load_env(env_path: str = ".env") -> None:
    path = Path(__file__).parent / env_path
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    path = Path(__file__).parent / config_path
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    return config


def get_settings() -> dict:
    load_env()
    config = load_config()

    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "telegram_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
        "clients_file": config.get(
            "storage", "clients_file", fallback="data/clients.json"
        ),
        "services_file": config.get(
            "storage", "services_file", fallback="data/services.json"
        ),
        "orders_file": config.get(
            "storage", "orders_file", fallback="data/orders.json"
        ),
        "export_dir": config.get("storage", "export_dir", fallback="exports/"),
        "currency": config.get("app", "currency", fallback="UAH"),
        "app_name": config.get("app", "name", fallback="Service Manager"),
        "app_version": config.get("app", "version", fallback="0.3.0"),
        "low_stock_threshold": config.getint(
            "inventory", "low_stock_threshold", fallback=5
        ),
    }