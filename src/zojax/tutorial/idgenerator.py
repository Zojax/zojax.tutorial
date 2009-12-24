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
from zope import interface, component
from zope.app.container.contained import NameChooser

from interfaces import IIdGenerator


class IDGenerator(object):
    interface.implements(IIdGenerator)

    _nextId = 1

    @property
    def nextId(self):
        id = self._nextId
        self._nextId += 1
        return u'%0.5d'%id


class NameChooser(NameChooser):
    component.adapts(IIdGenerator)

    def __init__(self, context):
        self.context = context

    def chooseName(self, name, object):
        return self.context.nextId
