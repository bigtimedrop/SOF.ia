import json

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            config.setdefault("voice_id", None)
            config.setdefault("rate", 150)
            config.setdefault("save_audio", True)
            return config
    except FileNotFoundError:
        return {
            "theme": "light",
            "voice_id": None,
            "rate": 150,
            "save_audio": True
        }


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
