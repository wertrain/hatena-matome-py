# -*- coding: utf-8 -*-
import json
import logging
import time
from my.util import hatena
from my.db import datastore
from datetime import datetime
from flask import Blueprint
apis = Blueprint('apis', __name__)

@apis.route('/system/hotentry')
def hotentry():
    hotentries = json.loads(hatena.fetch_hotentry())
    for entry in hotentries['responseData']['feed']['entries']:
        datastore.add_private_entry({
            'title': entry['title'],
            'url': entry['link'],
            'author': entry['author'],
            'content': entry['content'],
            'content_snippet': entry['contentSnippet'],
            'published_date': datetime.strptime(entry['publishedDate'], '%a, %d %b %Y %H:%M:%S -0700'),
            'categories': entry['categories']
        })
    return 'add entries.'

@apis.route('/system/openentry')
def openentry():
    private = datastore.get_private_entry()
    if private == None:
        logging.info('/system/openentry - no entry')
        return 'empty entry.'
    entry = json.loads(hatena.fetch_entry(private.url))
    public = datastore.publish_entry(private, {
        'eid': entry['eid'],
        'screenshot': entry['screenshot'],
        'bookmark_count': len(entry['bookmarks'])
    })
    comments = []
    for bookmark in entry['bookmarks']:
        if bookmark['comment']:
            # コメントからスターを取得する
            commentat = datetime.strptime(bookmark['timestamp'], '%Y/%m/%d %H:%M:%S')
            stars = hatena.fetch_comment_star(bookmark['user'], commentat, entry['eid'])
            # スター数が取れなかった場合 API の連続呼び出しで規制を受けた可能性がある
            if stars is None:
                logging.error('error - fetch_comment_star')
                return 'process interrupt';
            stars = json.loads(stars)
            # コメントがあるが、スター部分の形式が違うものがあるので除外
            if len(stars['entries']) == 0:
                continue
            datastore.add_bookmark_comment({
                'user': bookmark['user'],
                'comment': bookmark['comment'],
                'timestamp': commentat,
                'entry': public,
                'yellow_star_count': hatena.get_star_count(stars, 'yellow'),
                'green_star_count': hatena.get_star_count(stars, 'green'),
                'red_star_count': hatena.get_star_count(stars, 'red'),
                'blue_star_count': hatena.get_star_count(stars, 'blue')
            })
            time.sleep(0.1)
    return 'publish entry ' + public.url

@apis.route('/system/deleteall')
def deleteall():
    datastore.delete_all()
    return 'delete'