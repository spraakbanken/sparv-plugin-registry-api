
import requests
from base64 import b64decode
import yaml

MANIFESTS_URL = ("https://api.github.com/repos/spraakbanken/sparv-plugin-registry/git/trees/"
                 "d57100ca2f9d815e17dcb563e739b369f0165fd3")


def main():
    """Collect all manifest data from sparv-plungin-registry from GitHub."""
    manifests = []
    resp = requests.get(MANIFESTS_URL).json()
    manifests_list = resp.get("tree")
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
    return manifests


if __name__ == "__main__":
    manifests = main()
    from pprint import pprint
    for m in manifests:
        pprint(m)
