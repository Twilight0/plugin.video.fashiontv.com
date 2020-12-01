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


def check_inputstream_addon():

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    leia_plus = control.kodi_version() >= 18.0

    first_time_file = control.join(control.dataPath, 'first_time')

    if not addon_enabled and not file_exists(first_time_file) and leia_plus:

        try:

            yes = control.yesnoDialog(control.lang(30003))

            if yes:

                control.enable_addon('inputstream.adaptive')
                control.infoDialog(control.lang(30402))

            with open(first_time_file, 'a'):
                pass

        except Exception:

            pass


@urldispatcher.register('clear_cache')
def clear_cache():
    cache.clear(withyes=False, label_success=30084)


@urldispatcher.register('addBookmark', ['url'])
def addBookmark(url):

    bookmarks.add(url)


@urldispatcher.register('deleteBookmark', ['url'])
def deleteBookmark(url):

    bookmarks.delete(url)
