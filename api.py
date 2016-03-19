# -*- coding: utf-8 -*-
import json
import logging
import urllib
from google.appengine.api import memcache
from my.util import hatena

from flask import Blueprint
apis = Blueprint('apis', __name__)

@apis.route('/system/hotentry')
def hotentry():
    return hatena.get_hotentry()
