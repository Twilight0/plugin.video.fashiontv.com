# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

from sys import argv
from tulip.compat import parse_qsl
from tulip import bookmarks
# noinspection PyProtectedMember, PyUnresolvedReferences
from resources.lib import fashiontv

syshandle = int(argv[1])
sysaddon = argv[0]
params = dict(parse_qsl(argv[2][1:]))

########################################################################################################################

action = params.get('action')
url = params.get('url')

########################################################################################################################

if action is None:

    fashiontv.Indexer().root()

elif action == 'live':

    fashiontv.Indexer().live()

elif action == 'play':

    fashiontv.Indexer().play(url)

elif action == 'youtube':

    fashiontv.Indexer().yt(url)

elif action == 'cache_clear':

    from tulip.cache import clear
    clear(withyes=False)

elif action == 'addBookmark':

    bookmarks.add(url)

elif action == 'deleteBookmark':

    bookmarks.delete(url)

elif action == 'bookmarks':

    fashiontv.Indexer().bookmarks()
