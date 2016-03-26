# -*- coding: utf-8 -*-
u"""
    Google App Engine Datastore ラッパー
    __author__ = 'wertrain'
    __version__ = '0.1'
"""
import json
from google.appengine.ext import db

class EntryBase(db.Model):
    u"""
        エントリーの共通部分を表すデータ
    """
    title = db.StringProperty()
    url = db.LinkProperty()
    author = db.StringProperty()
    published_date = db.DateTimeProperty(auto_now_add=False)
    content = db.TextProperty()
    content_snippet = db.TextProperty()
    categories = db.StringListProperty(default=[])
    created_date = db.DateTimeProperty(auto_now_add=True)

class PrivateEntry(EntryBase):
    u"""
        公開前のエントリーを表すデータ
    """

class PublicEntry(EntryBase):
    u"""
        公開後のエントリーを表すデータ
    """
    eid = db.IntegerProperty()
    screenshot = db.LinkProperty()

class BookmarkComment(db.Model):
    hatena_id = db.StringProperty()
    comment = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now_add=False)
    entry = db.ReferenceProperty(PublicEntry)
    yellow_star_count = db.IntegerProperty(default=0)
    green_star_count = db.IntegerProperty(default=0)
    red_star_count = db.IntegerProperty(default=0)
    blue_star_count = db.IntegerProperty(default=0)

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

def add_bookmark_comment(param):
    comment = db.Query(BookmarkComment).filter('entry =', param.get('entry')).filter('hatena_id =', param.get('user')).get()
    if comment is None:
        comment = BookmarkComment()
    comment.hatena_id = param.get('user')
    comment.comment = param.get('comment')
    comment.timestamp = param.get('timestamp')
    comment.entry = param.get('entry')
    comment.yellow_star_count = param.get('yellow_star_count')
    comment.green_star_count = param.get('green_star_count')
    comment.red_star_count = param.get('red_star_count')
    comment.blue_star_count = param.get('blue_star_count')
    comment.put()
    return comment

def get_private_entry():
    return db.Query(PrivateEntry).get()

def get_public_entry(eid):
    return db.Query(PublicEntry).filter('eid =', eid).get()

def get_public_entries():
    entries = []
    for entry in PublicEntry.all().order('created_date'):
        entries.append(entry)
    return entries

def publish_entry(private, param):
    public = PublicEntry()
    public.title = private.title
    public.url = private.url
    public.author = private.author
    public.published_date = private.published_date
    public.content = private.content
    public.content_snippet = private.content_snippet
    public.categories = private.categories
    public.created_date = private.created_date
    public.eid = param.get('eid')
    public.screenshot = param.get('screenshot')
    private.delete()
    public.put()
    return public