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
    entries = datastore.get_public_entries()
    return render_template('home.html', entries=entries)

@app.route('/hotentries')
def hotentries():
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
    score = 0
    for comment in entry.bookmarkcomment_set:
        comments.append({
          'data': comment,
          'score': __style_from_score(hatena.get_star_score(comment)),
        })
    return render_template('entry.html', entry=entry, comments=comments)

def __style_from_score(score):
    """スコアを計算して、0-9の値を返す"""
    score_table = [70, 60, 50, 40, 35, 20, 10, 5, 1]
    for i, value in enumerate(score_table):
        if score > value:
            return len(score_table) - i
    return 0

@app.route('/category/<category>')
def category(category):
    """エントリーページを表示する"""
    return render_template('entry.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
