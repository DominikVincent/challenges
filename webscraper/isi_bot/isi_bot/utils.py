from pathlib import Path
from typing import Dict
import json

def read_config(path: Path) -> Dict:
    """Read config from yaml file."""
    with open(path) as f:
        config = json.load(f)
    return config