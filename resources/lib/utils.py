# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import
import json
from os.path import exists as file_exists
from tulip import control, bookmarks, cache
from tulip.url_dispatcher import urldispatcher
from base64 import b64decode
from zlib import decompress
from youtube_registration import register_api_keys
from .constants import scramble


def keys_registration():

    filepath = control.transPath(
        control.join(control.addon('plugin.video.youtube').getAddonInfo('profile'), 'api_keys.json')
    )

    setting = control.addon('plugin.video.youtube').getSetting('youtube.allow.dev.keys') == 'true'

    if file_exists(filepath):

        f = open(filepath)

        jsonstore = json.load(f)

        try:
            old_key_found = jsonstore['keys']['developer'][control.addonInfo('id')]['api_key'] == 'AIzaSyCE6qoV77uQMWR6g2mIVzjQs8wtqqa_KyM'
        except KeyError:
            old_key_found = False

        no_keys = control.addonInfo('id') not in jsonstore.get('keys', 'developer').get('developer') or old_key_found

        if setting and no_keys:

            keys = json.loads(decompress(b64decode(scramble)))

            register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])

            control.sleep(200)

        f.close()


@urldispatcher.register('clear_cache')
def clear_cache():
    cache.FunctionCache().reset_cache(notify=True)


@urldispatcher.register('addBookmark', ['url'])
def addBookmark(url):

    bookmarks.add(url)


@urldispatcher.register('deleteBookmark', ['url'])
def deleteBookmark(url):

    bookmarks.delete(url)
