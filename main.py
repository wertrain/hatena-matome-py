# -*- coding: utf-8 -*-
import logging
import pickle
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

# 1ページあたりに表示する記事件数
ENTRIES_PER_PAGE = 10

@app.route('/')
def home():
    memcache_key = 'public_entries';
    entries = memcache.get(memcache_key)
    if entries is None:
        entries = pickle.dumps(datastore.get_public_entries(limit=ENTRIES_PER_PAGE))
        memcache.add(memcache_key, entries, 60 * 60 * 24)
    entries = pickle.loads(str(entries))
    return render_template('home.html', entries=entries, sidebar_entries=__sidebar_entry(), page=0)

@app.route('/<page>')
def page(page):
    memcache_key = 'public_entries_' + page;
    entries = memcache.get(memcache_key)
    if entries is None:
        entries = pickle.dumps(datastore.get_public_entries(limit=ENTRIES_PER_PAGE, offset=(ENTRIES_PER_PAGE * int(page))))
        memcache.add(memcache_key, entries, 60 * 60 * 24)
    entries = pickle.loads(str(entries))
    return render_template('home.html', entries=entries, sidebar_entries=__sidebar_entry(), page=int(page))

@app.route('/popular')
def popular():
    memcache_key = 'get_popular_entries';
    entries = memcache.get(memcache_key)
    if entries is None:
        entries = pickle.dumps(datastore.get_popular_entries(limit=ENTRIES_PER_PAGE))
        memcache.add(memcache_key, entries, 60 * 60 * 24)
    entries = pickle.loads(str(entries))
    return render_template('home.html', entries=entries, sidebar_entries=__sidebar_entry(), page=0)

def __sidebar_entry():
    """サイドバー表示を管理"""
    memcache_key = 'public_entries';
    newer = memcache.get(memcache_key)
    if newer is None:
        newer = pickle.dumps(datastore.get_public_entries())
        memcache.add(memcache_key, newer, 60 * 60 * 24)
    newer = pickle.loads(str(newer))
    memcache_key = 'get_popular_entries';
    popular = memcache.get(memcache_key)
    if popular is None:
        popular = pickle.dumps(datastore.get_popular_entries())
        memcache.add(memcache_key, popular, 60 * 60 * 24)
    popular = pickle.loads(str(popular))
    return {'newer': newer[:6], 'popular': popular[:6]}

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
    return render_template('entry.html', entry=entry, comments=comments, sidebar_entries=__sidebar_entry())

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
    entries = datastore.get_public_entries_in_category(category)
    return render_template('home.html', entries=entries, sidebar_entries=__sidebar_entry())

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
