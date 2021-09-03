
import json
import time
from base64 import b64decode
from pathlib import Path

import requests
import yaml

MANIFESTS_URL = ("https://api.github.com/repos/spraakbanken/sparv-plugin-registry/git/trees/"
                 "d57100ca2f9d815e17dcb563e739b369f0165fd3")
CACHE_TIMEOUT_MINUTES = 15
TMP_DIR = Path(__file__).parent / "TEMP"
MANIFESTS_FILE = TMP_DIR / "manifests.json"


def main():
    """Get manifest data, either from cached file"""
    if MANIFESTS_FILE.is_file():
        cache_age = (time.time() - MANIFESTS_FILE.stat().st_mtime) / 60
        if cache_age < CACHE_TIMEOUT_MINUTES:
            return get_from_cache()
    # Get fresh data
    manifests = get_from_url()
    write_json(manifests)
    return manifests


def get_from_cache():
    """Get manifest data from cache file."""
    with open(MANIFESTS_FILE, "r") as f:
        return json.load(f)


def get_from_url():
    """Collect all manifest data from sparv-plungin-registry from GitHub."""
    manifests = []
    try:
        resp = requests.get(MANIFESTS_URL).json()
        manifests_list = resp.get("tree", [])
        for i in manifests_list:
            man_resp = requests.get(i.get("url")).json()
            content = b64decode(man_resp.get("content"))
            yamlcontent = yaml.load(content, Loader=yaml.FullLoader)
            if len(yamlcontent) == 1:
                # Manifest is a URL to the actual manifest
                man_url = yamlcontent.get("manifest")
                r = requests.get(man_url).content
                yamlcontent = yaml.load(r, Loader=yaml.FullLoader)

            manifests.append(yamlcontent)
    except Exception as e:
        print(f"Something went wrong: {e}")
    return manifests


def write_json(data):
    """Write json to a temporary file and move to correct place."""
    TMP_DIR.mkdir(exist_ok=True)
    tmp_file = MANIFESTS_FILE.with_suffix(MANIFESTS_FILE.suffix + ".tmp")
    with open(tmp_file, "w") as f:
        json.dump(data, f)
    Path.rename(tmp_file, MANIFESTS_FILE)


if __name__ == "__main__":
    manifests = main()
    from pprint import pprint
    for m in manifests:
        pprint(m)
