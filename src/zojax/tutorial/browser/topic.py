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
from zope import interface
from z3c.batching.batch import Batch
from zojax.layout.pagelet import BrowserPagelet
from zojax.content.browser.interfaces import IContentView

from seq import BTreeSequence


class TopicView(BrowserPagelet):
    interface.implements(IContentView)

    def update(self):
        context = self.context

        try:
            bstart = int(self.request.get('b_start', 0))
        except:
            bstart = 0

        self.messages = Batch(
            BTreeSequence(context), start=bstart,
            size=context.__parent__.topic_page_size)
