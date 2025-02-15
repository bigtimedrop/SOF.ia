import json

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"theme": "light"}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
