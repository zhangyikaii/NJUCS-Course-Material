import json
import os
from pathlib import Path

home = str(Path.home())
config_path = home + "/.scheme_editor"


def save_config(key, content):
    os.makedirs(config_path, exist_ok=True)
    with open(config_path + "/" + key + ".config", "w+") as f:
        f.write(json.dumps(content))


def load_config(key):
    with open(config_path + "/" + key + ".config", "r") as f:
        return json.loads(f.read())
