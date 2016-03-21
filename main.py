# -*- coding: utf-8 -*-
import logging
import json
import time
from api import apis
from datetime import datetime
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
        hotentries = hatena.fetch_hotentry()
        memcache.add(memcache_key, hotentries, 60 * 60 * 24)
    hotentries = json.loads(hotentries)
    return render_template('home.html', entries=hotentries)

@app.route('/entry/test')
def entry():
    """エントリーページを表示する"""
    entry = hatena.fetch_entry('http://shousha-ol.hatenadiary.jp/entry/2016/01/27/223746')
    entry = json.loads(entry)
    comments = []
    for bookmark in entry['bookmarks']:
        if bookmark['comment']:
            # コメントからスターを取得する
            commentat = datetime.strptime(bookmark['timestamp'], '%Y/%m/%d %H:%M:%S')
            stars = json.loads(hatena.fetch_comment_star(bookmark['user'], commentat, entry['eid']))
            # コメントがあるが、スター部分の形式が違うものがあるので除外
            if len(stars['entries']) == 0:
                continue
            comments.append({
                'at': commentat,
                'user': bookmark['user'],
                'comment': bookmark['comment'],
                'score': hatena.get_star_score(stars)
            })
            time.sleep(0.5)
    return render_template('entry.html', comments=reversed(comments))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
