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
"""Message Board Implementation

$Id$
"""
from zope import interface
from zojax.content.container import ContentContainer
from zojax.tutorial.interfaces import IMessageBoard
from zojax.tutorial.idgenerator import IDGenerator


class MessageBoard(IDGenerator, ContentContainer):
    """A very simple implementation of a message board topic """
    interface.implements(IMessageBoard)

    page_size = 10

    topic_page_size = 10
