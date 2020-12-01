# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json, re

from tulip import directory, client, cache, control, bookmarks as _bookmarks
from tulip.parsers import itertags_wrapper
from tulip.url_dispatcher import urldispatcher
from tulip.compat import iteritems
from .constants import *
from .utils import keys_registration


@urldispatcher.register('root')
def root():

    self_list = [
        {
            'title': control.lang(30001),
            'action': 'live'
        }
        ,
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
        ,
        {
            'title': control.lang(30005),
            'action': 'bookmarks',
            'icon': 'bookmarks.jpg'
        }
    ]

    plugin = 'plugin://plugin.video.youtube/channel/'
    clear_cache = {'title': 30002, 'query': {'action': 'clear_cache'}}

    for item in self_list:

        if item['action'] == 'youtube':
            item['url'] = ''.join([plugin, item['url'], '/?addon_id=', control.addonInfo('id')])

        item.update({'cm': [clear_cache]})

    directory.add(self_list)


@urldispatcher.register('bookmarks')
def bookmarks():

    self_list = _bookmarks.get()

    if not self_list:
        na = [{'title': control.lang(30007), 'action': None}]
        directory.add(na)
        return

    for i in self_list:
        bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
        bookmark['delbookmark'] = i['url']
        i.update({'cm': [{'title': 30006, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

    control.sortmethods()
    control.sortmethods('title')

    directory.add(self_list, content='videos')


def list_live_items():

    html = client.request(main_link)

    items = itertags_wrapper(html, 'article', attrs={'id': 'stream-.+'})

    self_list = []

    for item in items:

        url = itertags_wrapper(item.text, 'a', attrs={'class': 'live-stream-button full-overlay'}, ret='data-source')[0]

        title = itertags_wrapper(item.text, 'div', attrs={'class': 'a2a_kit a2a_kit_size_24 addtoany_list'}, ret='data-a2a-title')[0]
        title = client.replaceHTMLCodes(title)
        image = itertags_wrapper(item.text, 'img', attrs={'class': 'horizontal-thumbnail'}, ret='data-src')[0]

        data = {'title': title, 'image': image, 'url': url}

        self_list.append(data)

    return self_list


@urldispatcher.register('live')
def live():

    self_list = cache.get(list_live_items, 24)

    if self_list is None:
        return

    for item in self_list:

        item.update({'action': 'play', 'isFolder': 'False'})
        bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
        bookmark['delbookmark'] = item['url']
        item.update({'cm': [{'title': 30004, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

    control.sortmethods()
    control.sortmethods('title')

    directory.add(self_list, content='videos')


@urldispatcher.register('youtube', ['url'])
def yt(url):

    keys_registration()

    control.execute('Container.Update({},return)'.format(url))


def resolve(url):

    if 'megogo' in url:

        vid = re.search(r'id=(\d+)', url).group(1)
        url = 'https://embed.megogo.ru/aprx/stream?video_id={}'.format(vid)

    html = client.request(url)

    if 'megogo' in url:
        js = json.loads(html)
        stream = js.get('data', {}).get('src')
    else:
        stream = 'https:' + re.search(r"'(.+m3u8)'", html).group(1)

    return stream


@urldispatcher.register('play', ['url'])
def play(url):

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    mimetype = None
    manifest_type = None

    leia_plus = control.kodi_version() >= 18.0

    stream = resolve(url)

    if '.m3u8' in stream:

        manifest_type = 'hls'
        mimetype = 'application/vnd.apple.mpegurl'

    elif '.mpd' in stream:

        manifest_type = 'mpd'

    dash = addon_enabled and ('.m3u8' in stream or '.mpd' in stream)

    directory.resolve(stream, dash=dash and leia_plus, mimetype=mimetype, manifest_type=manifest_type)
