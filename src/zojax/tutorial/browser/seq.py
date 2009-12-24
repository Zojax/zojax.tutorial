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
from zope.proxy import removeAllProxies
from zope.interface.common.sequence import IFiniteSequence


class BTreeSequence(object):
    interface.implements(IFiniteSequence)

    def __init__(self, btree):
        self.btree = btree
        self.length = len(btree)
        self.sequence = removeAllProxies(btree).keys()

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        if idx > self.length:
            raise IndexError(idx)
        return self.btree[self.sequence[idx]]
