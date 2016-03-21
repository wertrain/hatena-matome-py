# -*- coding: utf-8 -*-
u"""
    はてな関連ユーティリティ
    __author__ = 'wertrain'
    __version__ = '0.1'
"""
import json
import urllib
import logging
import re
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import urlfetch

def __urlfetch(url):
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return result.content
    else:
        logging.error(str(result.status_code) + ':' + result.content)
    return None

def fetch_hotentry(num=20):
    u"""
        ホットエントリーを取得する
    """
    url = 'https://ajax.googleapis.com/ajax/services/feed/load?v=1.0&q=http://b.hatena.ne.jp/hotentry.rss&num=' + str(num)
    return __urlfetch(url)

def fetch_entry(url):
    u"""
        エントリーを取得する
    """
    apilite = 'http://b.hatena.ne.jp/entry/jsonlite/?url=' + url
    return __urlfetch(apilite)

def fetch_comment_star(id, date, eid):
    u"""
        コメントについたスターを取得する
    """
    url = 'http://b.hatena.ne.jp/' + id + '/' + date.strftime('%Y%m%d') + '#bookmark-' + str(eid)
    apiurl = 'http://s.hatena.com/entry.json?uri=' + urllib.quote(url)
    return __urlfetch(apiurl)

def get_star_score(result):
    u"""
        スターからスコアを計算する
    """
    score = 0;
    if len(result['entries']) == 0:
        return score
    score += len(result['entries'][0]['stars'])
    if 'colored_stars' not in result['entries'][0]:
        return score
    table = {'blue': 10, 'red': 6, 'green': 2}
    for colored in result['entries'][0]['colored_stars']:
        score += len(colored['stars']) * table[colored['color']]
    return score

_quote_by_backslash = re.compile(u'([\'"\\\\])')
def quote_by_backslash(s):
    return _quote_by_backslash.sub(ur'\\\1', s)

_remove_backslash = re.compile(ur'\\(.)')
def remove_backslash(s):
    return _remove_backslash.sub(ur'\1', s)
