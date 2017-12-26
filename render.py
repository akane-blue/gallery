#!/usr/bin/env python
# -*- coding: utf-8 -*-

GALLERY_JSON = 'gallery.json'

import re
import json
from jinja2 import Environment, FileSystemLoader

# Custom filter method
def regex_replace(s, find, replace):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)

env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
env.filters['regex_replace'] = regex_replace

template = env.get_template('index.html.j2')

akanes=[]
with open(GALLERY_JSON, 'r') as f:
    akanes=json.load(f)

html = template.render(akanes=akanes)

with open("index.html", "w") as f:
    f.write(html)
