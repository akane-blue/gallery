#!/usr/bin/env python
# -*- coding: utf-8 -*-

GALLERY_JSON = 'gallery.json'

import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
template = env.get_template('index.html.j2')

akanes=[]
with open(GALLERY_JSON, 'r') as f:
    akanes=json.load(f)

html = template.render(akanes=akanes)

with open("index.html", "w") as f:
    f.write(html)
