# -*- coding: utf-8 -*-
u"""
    Google App Engine Datastore ラッパー
    __author__ = 'wertrain'
    __version__ = '0.1'
"""
import json
from google.appengine.ext import db

class PrivateEntry (db.Model):
    u"""
        公開前のエントリーを表すデータ
    """
    title = db.StringProperty()
    url = db.StringProperty()
    author = db.StringProperty()
    published_date = db.DateTimeProperty(auto_now_add=False)
    content = db.TextProperty()
    content_snippet = db.TextProperty()
    categories = db.StringListProperty(default=[])

def add_private_entry(param):
    entry = db.Query(PrivateEntry).filter('url =', param.get('url')).get()
    if entry is not None:
        return entry
    entry = PrivateEntry()
    entry.title = param.get('title')
    entry.url = param.get('url')
    entry.author = param.get('author')
    entry.published_date = param.get('published_date')
    entry.content = param.get('content')
    entry.content_snippet = param.get('content_snippet')
    entry.categories = param.get('categories')
    entry.put()
    return entry
