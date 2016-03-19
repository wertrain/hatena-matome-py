# -*- coding: utf-8 -*-
import json
import logging
import urllib
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from flask import Blueprint
apis = Blueprint('apis', __name__)

@apis.route('/system/hotentry')
def hotentry():
    url = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&q=http://b.hatena.ne.jp/hotentry.rss'
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return result.content
    else:
        logging.error('/system/hotentry - ' + result.status_code)
    return None

