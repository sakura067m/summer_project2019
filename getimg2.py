import sys
import requests
from urllib.parse import urlencode,parse_qs,urlparse
import lxml.html
import json

if __name__ == "__main__":
    target = "Fuji_list.txt"
    with open(target, "r") as f:
        order = f.readlines()

    for l in order[1:]:
        img_url = l.split()[]
        res = requests.get(img_url)
        with open(save_name, "wb") as fout:
            fout.write(res.content)

        break
