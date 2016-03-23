# -*- coding: utf-8 -*-
import logging
import json
import time
from api import apis
from datetime import datetime
from flask import Flask, render_template
from my.util import hatena
from my.db import datastore
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
        hotentries = hatena.fetch_hotentry()
        memcache.add(memcache_key, hotentries, 60 * 60 * 24)
    hotentries = json.loads(hotentries)
    return render_template('home.html', entries=hotentries)

@app.route('/entry/<eid>')
def entry(eid):
    """エントリーページを表示する"""
    entry = datastore.get_public_entry(int(eid))
    comments = []   
    for comment in entry.bookmarkcomment_set:
        comments.append(comment)
    return render_template('entry.html', entry=entry, comments=comments)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
