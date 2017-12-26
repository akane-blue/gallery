#!/usr/bin/env python3
import requests
import json
import pyjade
import os.path
from urllib.parse import urlparse
import hashlib
from time import sleep
from PIL import Image
from io import BytesIO
from datetime import datetime

with open("./list.txt", "r") as f:
    urls = f.read().split("\n")
urls = list(set(urls)) # unique
akanes = []

for url in urls:
    if not url.startswith("http"):
        continue
    cache_file_name = "cache/ap/" + url.replace("https://", "").replace("http://", "").replace("/", "_").replace("@", "") + ".json"
    if not os.path.exists(cache_file_name):
        print("fetching "+url+" ...")
        r = requests.get(url, headers = {
            "Accept": "application/activity+json"
        }).json()
        with open(cache_file_name, "w") as f:
            json.dump(r, f)
        sleep(1)
    r = json.load(open(cache_file_name))
    for attachment in r.get("attachment", []):
        if not attachment.get("mediaType", "").startswith("image/"): # not image
            continue
        img_url = urlparse(attachment["url"])
        img_file = img_url.hostname + "_" + hashlib.sha1(attachment["url"].encode("utf-8")).hexdigest()
        if not os.path.exists("img/"+img_file+".png"):
            print("fetching image "+attachment["url"]+" ...")
            img_req = requests.get(attachment["url"])
            img_req.raise_for_status()
            sleep(1)
            img = Image.open(BytesIO(img_req.content))
            img.save("img/"+img_file+".png")
        if not os.path.exists("img/thumbnail/"+img_file+".jpg"):
            with open("img/"+img_file+".png", "rb") as f:
                img = Image.open(f)
                img = img.convert("RGB")
                img.thumbnail((600, 600))
                img.save("img/thumbnail/"+img_file+".jpg",quality=75)
        akanes.append({
            "img": img_file,
            "original": url,
            "unix": datetime.strptime(r["published"], "%Y-%m-%dT%H:%M:%SZ").timestamp()
        })

print(akanes)

akanes = sorted(akanes, key=lambda x:x["unix"], reverse = True)

from pyjade.parser import Parser
from pyjade.ext.html import HTMLCompiler, local_context_manager

def process(jade_string, context=None, **compiler_kwargs):
    ctx = context or {}
    block = Parser(jade_string).parse()
    compiler = HTMLCompiler(block, **compiler_kwargs)
    with local_context_manager(compiler, ctx):
        return compiler.compile()

with open("base.pug", "r") as f_pug:
    html = process(f_pug.read(), {"akanes": akanes})
    with open("index.html", "w") as f_html:
        f_html.write(html)
with open("list.json", "w") as f:
    json.dump(akanes, f)