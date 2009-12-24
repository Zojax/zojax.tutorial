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
from zojax.layout.pagelet import BrowserPagelet
from zojax.content.browser.interfaces import IContentView
from zojax.tutorial.interfaces import IMessage


class MessageView(BrowserPagelet):
    interface.implements(IContentView)

    def render(self):
        return IMessage['body'].render(self.context)

    def __call__(self):
        self.redirect('../')
        return super(MessageView, self).__call__()
