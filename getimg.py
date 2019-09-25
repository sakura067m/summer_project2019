import sys
import requests
from urllib.parse import urlencode,parse_qs,urlparse
import lxml.html
import json

if __name__ == "__main__":
    target = "Fuji_list.txt"
    with open(target, "r") as f:
        order = f.readlines()

    selector = '//*[@id="react-root"]'
    '/section/main/article/div/div[1]/div[*]/a[*]'

    for l in order:
        post_url = l[:-1]
        print(post_url)
        res = requests.get(post_url)
        post_html = lxml.html.fromstring(res.content)
        imgs = post_html.cssselect("a")
        print(imgs)
        elms = post_html.xpath(selector)
        for elm in elms:
            pass

        break
