# -*- coding: utf-8 -*-
import json
import logging
import urllib
from google.appengine.api import memcache
from my.util import hatena
from my.db import datastore
from datetime import datetime
from flask import Blueprint
apis = Blueprint('apis', __name__)

@apis.route('/system/hotentry')
def hotentry():
    hotentries = json.loads(hatena.fetch_hotentry())
    for entry in hotentries['responseData']['feed']['entries']:
        datastore.add_private_entry({
            'title': entry['title'],
            'url': entry['link'],
            'author': entry['author'],
            'content': entry['content'],
            'content_snippet': entry['contentSnippet'],
            'published_date': datetime.strptime(entry['publishedDate'], '%a, %d %b %Y %H:%M:%S -0700'),
            'categories': []
        })
    return 'add entries.'
