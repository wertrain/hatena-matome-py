# -*- coding: utf-8 -*-
u"""
    はてな関連ユーティリティ
    __author__ = 'wertrain'
    __version__ = '0.1'
"""
import json
from google.appengine.ext import db
from google.appengine.api import urlfetch

def get_hotentry(num=20):
    u"""
        ホットエントリーを取得する
    """
    url = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&q=http://b.hatena.ne.jp/hotentry.rss&num=' + str(num)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return result.content
    else:
        logging.error('get_hotentry - ' + result.status_code)
    return None

def get_entry(url):
    u"""
        エントリーを取得する
    """
    apilite = 'http://b.hatena.ne.jp/entry/jsonlite/?url=' + url
    result = urlfetch.fetch(apilite)
    if result.status_code == 200:
        return result.content
    else:
        logging.error('get_entry - ' + result.status_code)
    return None
