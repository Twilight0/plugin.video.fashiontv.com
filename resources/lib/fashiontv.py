# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import json, re
from os.path import exists as file_exists
from tulip import directory, client, cache, control, bookmarks
from tulip.parsers import itertags_wrapper
from tulip.compat import iteritems
from base64 import b64decode
from zlib import decompress
from youtube_registration import register_api_keys


class Indexer:

    def __init__(self):

        self.list = []
        self.main_link = 'https://www.fashiontv.com/'
        self.fashion_tv_yt_channel = 'UCqzju-_WMKsgNx8R3QwupQQ'
        self.ftv_yt_channel = 'UClnblsrZrugJfFs4ANPgNcA'
        self.ftv_hot_yt_channel = 'UCDN6BTcfgHDuBQgCgXkU-cA'
        self.ftv_parties_yt_channel = 'UCLiyW3PZFDSxIw6EES8MneQ'
        self.ftv_asia_yt_channel = 'UCC2Iic6b-nhY7CSRUm_nyng'
        self.ftv_news_channel = 'UCi12i9eiWFh67T-uCP1y7Gw'
        self.scramble = (
            'eJwVzNsKgjAAANBfkT2XTMW59SYSYmWgkdGTjDnmfeomMaN/Dz/gnC9oKnCyAPIQDBzi+xB5R8hmriBkNUHSHT1PuBBL'
            '7NS+I4l2MLLpNClbSCl6viq+MDlqPmqbyQEcLECnpuy42dsw2ejDRGc0yyII1ix95Ui4Q1JsbabwR88zLa8m3ZXibOF6R'
            '2/TB2HcVreCXkS8LU/Y5RG5b+D3Bwj/Nu0='
        )

        self.keys_registration()
        self.check_inputstream_addon()

    def root(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'live'
            }
            ,
            {
                'title': 'Fashion TV',
                'action': 'youtube',
                'image': 'https://yt3.ggpht.com/a/AATXAJxZonaXhogfs_ioQnbxlhR7NpepOecdrBYzbHmOm1k=s256',
                'url': self.fashion_tv_yt_channel,
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': 'FTV',
                'action': 'youtube',
                'image': 'https://yt3.ggpht.com/a/AATXAJxLtsDGDS6pB9XFt_2wIe3UrG9BU3UW7qVscEQgSg=s256',
                'url': self.ftv_yt_channel,
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': 'FTV HOT',
                'action': 'youtube',
                'image': 'https://yt3.ggpht.com/a/AATXAJxJIFyHhkMeUbmMEIahbXB8tOe5rQOHMIYjvFh21w=s256',
                'url': self.ftv_hot_yt_channel,
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': 'FashionTV Parties',
                'action': 'youtube',
                'image': 'https://yt3.ggpht.com/a/AATXAJwiPGuSb3438Ql1kh1Je6YLaWj52skL7MKHgaUJ=s256',
                'url': self.ftv_parties_yt_channel,
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': 'FashionTV Asia',
                'action': 'youtube',
                'image': 'https://yt3.ggpht.com/a/AATXAJxhBT9-z8FzvWbOZqbwzlKMaG9ib7NdRQVvhu3T=s256',
                'url': self.ftv_parties_yt_channel,
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': 'FashionTV News',
                'action': 'youtube',
                'image': 'https://yt3.ggpht.com/a/AATXAJxw6UfiplqVo8OHZdMhoZAPOwcyjiKQQSYbdOaH=s256',
                'url': self.ftv_news_channel,
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
        cache_clear = {'title': 30002, 'query': {'action': 'cache_clear'}}

        for item in self.list:

            if item['action'] == 'youtube':
                item['url'] = ''.join([plugin, item['url'], '/?addon_id=', control.addonInfo('id')])

            item.update({'cm': [cache_clear]})

        directory.add(self.list)

    def bookmarks(self):

        self.list = bookmarks.get()

        if not self.list:
            na = [{'title': control.lang(30007), 'action': None}]
            directory.add(na)
            return

        for i in self.list:
            bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
            bookmark['delbookmark'] = i['url']
            i.update({'cm': [{'title': 30006, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

        control.sortmethods()
        control.sortmethods('title')

        directory.add(self.list, content='videos')

    def list_live_items(self):

        html = client.request(self.main_link)

        items = itertags_wrapper(html, 'article', attrs={'id': 'stream-.+'})

        for item in items:

            url = itertags_wrapper(item.text, 'a', attrs={'class': 'live-stream-button full-overlay'}, ret='data-source')[0]

            title = itertags_wrapper(item.text, 'div', attrs={'class': 'a2a_kit a2a_kit_size_24 addtoany_list'}, ret='data-a2a-title')[0]
            title = client.replaceHTMLCodes(title)
            image = itertags_wrapper(item.text, 'img', attrs={'class': 'horizontal-thumbnail'}, ret='data-src')[0]

            data = {'title': title, 'image': image, 'url': url}

            self.list.append(data)

        return self.list

    def live(self):

        self.list = cache.get(self.list_live_items, 24)

        if self.list is None:
            return

        for item in self.list:

            item.update({'action': 'play', 'isFolder': 'False'})
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['delbookmark'] = item['url']
            item.update({'cm': [{'title': 30004, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

        control.sortmethods()
        control.sortmethods('title')

        directory.add(self.list, content='videos')

    @staticmethod
    def yt(url):

        control.execute('Container.Update({},return)'.format(url))

    @staticmethod
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

    def play(self, url):

        try:
            addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
        except KeyError:
            addon_enabled = False

        mimetype = None
        manifest_type = None

        leia_plus = control.kodi_version() >= 18.0

        stream = self.resolve(url)

        if '.m3u8' in stream:

            manifest_type = 'hls'
            mimetype = 'application/vnd.apple.mpegurl'

        elif '.mpd' in stream:

            manifest_type = 'mpd'

        dash = addon_enabled and ('.m3u8' in stream or '.mpd' in stream)

        directory.resolve(stream, dash=dash and leia_plus, mimetype=mimetype, manifest_type=manifest_type)

    def keys_registration(self):

        filepath = control.transPath(control.join(control.addon('plugin.video.youtube').getAddonInfo('profile'), 'api_keys.json'))

        setting = control.addon('plugin.video.youtube').getSetting('youtube.allow.dev.keys') == 'true'

        if file_exists(filepath):

            f = open(filepath)
    
            jsonstore = json.load(f)

            no_keys = control.addonInfo('id') not in jsonstore.get('keys', 'developer').get('developer')

            if setting and no_keys: 
    
                keys = json.loads(decompress(b64decode(self.scramble)))
    
                register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])
    
            f.close()

    @staticmethod
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
