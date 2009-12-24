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
"""Message Board Interfaces

Interfaces for the zojax based Message Board Package

$Id$
"""
from zope import schema, interface
from zojax.richtext.field import RichText
from zojax.content.interfaces import IItem


class IMessage(interface.Interface):
    """A message object."""

    title = schema.TextLine(
        title=u"Title/Subject",
        description=u"Title and/or subject of the message.",
        default=u"",
        required=True)

    body = RichText(
        title=u"Message Body",
        description=u"This is the actual message. Type whatever you wish.",
        default=u"",
        required=False)


class IIdGenerator(interface.Interface):
    """ generate ids for it's contents """

    nextId = interface.Attribute('nextId')


class ITopic(IItem, IIdGenerator):
    """ A topic object """


class IMessageBoard(IItem, IIdGenerator):
    """The message board is the base object for our package. It can only
    contain ITopic objects."""

    # we need this just to replace `title` and `description` for field
    description = schema.Text(
        title=u"Description",
        description=u"A detailed description of the content of the board.",
        default=u"",
        required=False)


class IMessageBoardConfiglet(interface.Interface):

    forum_page_size = schema.Int(
        title = u'Forum page size',
        description = u'Number of topic per page.',
        default = 20,
        required = False)
