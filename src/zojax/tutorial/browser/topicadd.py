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
from zope.component import getUtility
from zojax.content.interfaces import IContentType
from zojax.content.forms.form import Fields, AddForm

from zojax.tutorial.interfaces import ITopic, IMessage


class AddTopicForm(AddForm):

    fields = Fields(ITopic, IMessage['body'])

    def create(self, data):
        topic = self.context.create(
            data.get('title'), data.get('description'))

        messageType = getUtility(IContentType, 'zojax.tutorial.Message')

        message = messageType.create(data['title'])
        message.body = data['body']
        self._message = message

        return topic

    def add(self, object):
        topic = super(AddTopicForm, self).add(object)

        topic[topic.nextId] = self._message
        return topic
