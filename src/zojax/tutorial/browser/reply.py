##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope.component import getMultiAdapter
from zojax.layout.pagelet import BrowserPagelet
from zojax.content.browser.interfaces import IContentAdding


class ReplyForm(BrowserPagelet):

    def render(self):
        adding = getMultiAdapter((self.context, self.request), IContentAdding)
        ctype = adding.getContentType('zojax.tutorial.Message')

        form = getMultiAdapter((ctype, self.request), name='index.html')
        form.update()
        if form.isRedirected:
            self.redirect()

        return form.render()
