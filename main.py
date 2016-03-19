# -*- coding: utf-8 -*-
import logging
import json
from api import apis
from flask import Flask, render_template
from my.util import hatena
from google.appengine.api import memcache

app = Flask(__name__)
app.register_blueprint(apis)
app.config['DEBUG'] = True

logging.getLogger().setLevel(logging.DEBUG)

@app.route('/')
def home():
    """トップページを表示する"""
    memcache_key = 'hotentries';
    hotentries = memcache.get(memcache_key)
    if hotentries is None:
        hotentries = hatena.get_hotentry()
        memcache.add(memcache_key, hotentries, 60 * 60 * 24)
    hotentries = json.loads(hotentries)
    return render_template('home.html', test='aa',entries=hotentries)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
