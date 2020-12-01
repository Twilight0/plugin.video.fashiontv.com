# -*- coding: utf-8 -*-

'''
    Fashion TV Player Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

import sys
from tulip.compat import parse_qsl
from tulip.url_dispatcher import urldispatcher
# noinspection PyProtectedMember, PyUnresolvedReferences
from resources.lib import fashiontv, utils


def main(argv=None):

    if sys.argv: argv = sys.argv

    utils.check_inputstream_addon()

    params = dict(parse_qsl(argv[2][1:]))
    action = params.get('action', 'root')
    urldispatcher.dispatch(action, params)


if __name__ == '__main__':

    sys.exit(main())
