# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json

from tulip import directory, client, cache, control, bookmarks as bms
from tulip.url_dispatcher import urldispatcher
from tulip.compat import iteritems, is_py3
from tulip.fuzzywuzzy import process
from .constants import *
from .utils import keys_registration


cache_function = cache.FunctionCache().cache_function


@urldispatcher.register('root')
def root():

    self_list = [
        {
            'title': control.lang(30001),
            'action': 'main'
        }
        ,
        {
            'title': control.lang(30009),
            'action': 'playlist',
            'query': '["10091955", "9243425", "10091952", "9243291", "9243509", "9243272", "10041248"]',
            'icon': 'live.jpg'
        }
        ,
        {
            'title': control.lang(30010),
            'action': 'search',
            'icon': 'search.jpg'
        }
        ,
        {
            'title': control.lang(30003),
            'action': 'yt_channels',
            'image': 'https://yt3.ggpht.com/a/AATXAJxLtsDGDS6pB9XFt_2wIe3UrG9BU3UW7qVscEQgSg=s256'
        }
        ,
        {
            'title': control.lang(30005),
            'action': 'bookmarks',
            'icon': 'bookmarks.jpg'
        }
    ]

    for item in self_list:
        clear_cache = {'title': 30002, 'query': {'action': 'clear_cache'}}
        item.update({'cm': [clear_cache]})

    directory.add(self_list)


@urldispatcher.register('yt_channels')
def yt_channels():

    self_list = [
        {
            'title': 'Fashion TV',
            'action': 'youtube',
            'image': 'https://yt3.ggpht.com/a/AATXAJxZonaXhogfs_ioQnbxlhR7NpepOecdrBYzbHmOm1k=s256',
            'url': fashion_tv_yt_channel,
            'isFolder': 'False', 'isPlayable': 'False'
        }
        ,
        {
            'title': 'FTV',
            'action': 'youtube',
            'image': 'https://yt3.ggpht.com/a/AATXAJxLtsDGDS6pB9XFt_2wIe3UrG9BU3UW7qVscEQgSg=s256',
            'url': ftv_yt_channel,
            'isFolder': 'False', 'isPlayable': 'False'
        }
        ,
        {
            'title': 'FTV HOT',
            'action': 'youtube',
            'image': 'https://yt3.ggpht.com/a/AATXAJxJIFyHhkMeUbmMEIahbXB8tOe5rQOHMIYjvFh21w=s256',
            'url': ftv_hot_yt_channel,
            'isFolder': 'False', 'isPlayable': 'False'
        }
        ,
        {
            'title': 'FashionTV Parties',
            'action': 'youtube',
            'image': 'https://yt3.ggpht.com/a/AATXAJwiPGuSb3438Ql1kh1Je6YLaWj52skL7MKHgaUJ=s256',
            'url': ftv_parties_yt_channel,
            'isFolder': 'False', 'isPlayable': 'False'
        }
        ,
        {
            'title': 'FashionTV Asia',
            'action': 'youtube',
            'image': 'https://yt3.ggpht.com/a/AATXAJxhBT9-z8FzvWbOZqbwzlKMaG9ib7NdRQVvhu3T=s256',
            'url': ftv_parties_yt_channel,
            'isFolder': 'False', 'isPlayable': 'False'
        }
        ,
        {
            'title': 'FashionTV News',
            'action': 'youtube',
            'image': 'https://yt3.ggpht.com/a/AATXAJxw6UfiplqVo8OHZdMhoZAPOwcyjiKQQSYbdOaH=s256',
            'url': ftv_news_channel,
            'isFolder': 'False', 'isPlayable': 'False'
        }
    ]

    plugin = 'plugin://plugin.video.youtube/channel/'

    for item in self_list:

        item['url'] = ''.join([plugin, item['url'], '/?addon_id=', control.addonInfo('id')])

    directory.add(self_list)


@urldispatcher.register('bookmarks')
def bookmarks():

    self_list = bms.get()

    if not self_list:
        na = [{'title': control.lang(30007), 'action': None}]
        directory.add(na)
        return

    for i in self_list:
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        try:
            bookmark['delbookmark'] = i['url']
        except KeyError:
            bookmark['delbookmark'] = i['query']
        i.update({'cm': [{'title': 30006, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

    control.sortmethods()
    control.sortmethods('title')

    directory.add(self_list, content='videos')


@cache_function(3660)
def loader():

    _json = client.request(main_json, output='json')

    pls = list(_json['playlists'].values())
    content = list(_json['content'].values())

    _playlists = []
    contents = []

    for p in pls:

        if not p.get('detailedCarousel'):
            continue
        data = {'title': p['name'], 'query': json.dumps(p['itemIds'])}

        _playlists.append(data)

    for c in content:

        vid = c['id']
        title = c['title']
        plot = c['description']
        image = c['thumbnail_playlist']
        duration = ['videoDuration']
        is_live = ['is_live_streaming']
        url = c['streamURL']
        fanart = c['thumbnail']

        data = {
            'title': title, 'plot': plot, 'image': image, 'duration': duration,
            'is_live': is_live, 'url': url, 'id': vid, 'fanart': fanart
        }
        contents.append(data)

    return _playlists, contents


@urldispatcher.register('main')
def main():

    self_list = loader()[0]

    for i in self_list:
        i.update({'action': 'playlist'})
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        bookmark['bookmark'] = i['query']
        i.update({'cm': [{'title': 30004, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

    control.sortmethods()
    control.sortmethods('title')

    directory.add(self_list, content='videos')


@urldispatcher.register('playlist', ['query'])
def playlist(query):

    self_list = loader()[1]

    query = json.loads(query)

    videos = [i for i in self_list if i['id'] in query]

    for i in videos:
        i.update({'action': 'play', 'isFolder': 'False'})
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        bookmark['bookmark'] = i['url']
        i.update({'cm': [{'title': 30004, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

    control.sortmethods()
    control.sortmethods('title')

    directory.add(videos, content='movies')


@urldispatcher.register('search')
def search():

    input_str = control.inputDialog()

    if not input_str:
        return

    items = loader()[1]

    if is_py3:

        titles = [i['title'] for i in items]

        matches = [
            titles.index(t) for t, s in process.extract(
                input_str, titles, limit=20
            ) if s >= 60
        ]

    else:

        titles = [i['title'].encode('unicode-escape') for i in items]

        matches = [
            titles.index(t) for t, s in process.extract(
                input_str.encode('unicode-escape'), titles, limit=20
            ) if s >= 60
        ]

    data = []

    for m in matches:
        data.append(items[m])

    if not data:

        control.infoDialog(30011)

        return

    else:

        for i in data:
            i.update({'action': 'play', 'isFolder': 'False'})
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['bookmark'] = i['url']
            i.update({'cm': [{'title': 30501, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

        control.sortmethods('title')
        directory.add(data, infotype='movies')


@urldispatcher.register('youtube', ['url'])
def yt(url):

    keys_registration()

    control.execute('Container.Update({},return)'.format(url))


@urldispatcher.register('play', ['url'])
def play(url):

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    mimetype = None
    manifest_type = None

    leia_plus = control.kodi_version() >= 18.0

    if '.m3u8' in url:

        manifest_type = 'hls'
        mimetype = 'application/vnd.apple.mpegurl'

    elif '.mpd' in url:

        manifest_type = 'mpd'

    dash = addon_enabled and ('.m3u8' in url or '.mpd' in url)

    directory.resolve(url, dash=dash and leia_plus, mimetype=mimetype, manifest_type=manifest_type)
