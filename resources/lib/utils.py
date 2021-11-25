# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import
import json
from tulip import control, bookmarks, cache
from tulip.url_dispatcher import urldispatcher
from base64 import b64decode
from zlib import decompress
from youtube_registration import register_api_keys
from .constants import scramble


def keys_registration():

    keys = json.loads(decompress(b64decode(scramble)))

    register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])


@urldispatcher.register('clear_cache')
def clear_cache():
    cache.FunctionCache().reset_cache(notify=True)


@urldispatcher.register('addBookmark', ['url'])
def addBookmark(url):

    bookmarks.add(url)


@urldispatcher.register('deleteBookmark', ['url'])
def deleteBookmark(url):

    bookmarks.delete(url)
