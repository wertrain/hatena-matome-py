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
    content = hatena.remove_backslash(u'<blockquote title=\"はあちゅう 公式ブログ - 旅で人生が変わったとか言う人は中身がゼロなのです - Powered by LINE\"><cite><img src=\"http://cdn-ak.favicon.st-hatena.com/?url=http%3A%2F%2Flineblog.me%2F\" alt=\"\"> <a href=\"http://lineblog.me/ha_chu/archives/56947577.html\">はあちゅう 公式ブログ - 旅で人生が変わったとか言う人は中身がゼロなのです - Powered by LINE</a></cite><p><a href=\"http://lineblog.me/ha_chu/archives/56947577.html\"><img src=\"http://cdn-ak.b.st-hatena.com/entryimage/282693361-1458472448.jpg\" alt=\"はあちゅう 公式ブログ - 旅で人生が変わったとか言う人は中身がゼロなのです - Powered by LINE\" title=\"はあちゅう 公式ブログ - 旅で人生が変わったとか言う人は中身がゼロなのです - Powered by LINE\"></a></p><p>はあちゅう @ha_chu 海外にやたら行く自己啓発系の人って「旅＝クリエイティブ！クリエイティブな私に、ほらみんな！憧れて！！」というオーラを発しているんだけど、ひとつの場所で淡々と仕事するほうがよっぽどクリエイティブだと思う。私は仕事が好きな人が好きだし、旅人の言葉より仕事人の言葉のほうに重みを感じる 2016/03/20 18:29:41 はあちゅう @ha_chu 旅での刺激は外部からもら...</p><p><a href=\"http://b.hatena.ne.jp/entry/http://lineblog.me/ha_chu/archives/56947577.html\"><img src=\"http://b.hatena.ne.jp/entry/image/http://lineblog.me/ha_chu/archives/56947577.html\" alt=\"はてなブックマーク - はあちゅう 公式ブログ - 旅で人生が変わったとか言う人は中身がゼロなのです - Powered by LINE\" title=\"はてなブックマーク - はあちゅう 公式ブログ - 旅で人生が変わったとか言う人は中身がゼロなのです - Powered by LINE\" border=\"0\" style=\"border:none\"></a> <a href=\"http://b.hatena.ne.jp/append?http://lineblog.me/ha_chu/archives/56947577.html\"><img src=\"http://b.hatena.ne.jp/images/append.gif\" border=\"0\" alt=\"はてなブックマークに追加\" title=\"はてなブックマークに追加\"></a></p></blockquote><img src=\"http://feeds.feedburner.com/~r/hatena/b/hotentry/~4/al_CorpWOxY\" height=\"1\" width=\"1\" alt=\"\">')
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
    return render_template('entry.html', content=content, comments=reversed(comments))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
