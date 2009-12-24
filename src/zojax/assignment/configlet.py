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
from zope import interface, component, event
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.intid.interfaces import IIntIds, IIntIdRemovedEvent

from assignments import Assignments
from interfaces import IAssignmentsAware, IAssignmentsConfiglet


class AssignmentsConfiglet(object):
    interface.implements(IAssignmentsConfiglet)

    def getAssignmentsFor(self, context):
        id = getUtility(IIntIds).queryId(removeAllProxies(context))
        if id is None:
            return

        name = str(id)

        assingments = self.data.get(name)
        if assingments is None:
            assingments = Assignments(id)
            event.notify(ObjectCreatedEvent(assingments))
            self.data[name] = assingments
            assingments = self.data[name]

        return assingments

    def removeAssignmentsFor(self, context):
        id = getUtility(IIntIds).queryId(removeAllProxies(context))
        if id is None:
            return

        if str(id) in self.data:
            del self.data[str(id)]


@component.adapter(IAssignmentsAware, IIntIdRemovedEvent)
def unindexDocSubscriber(object, ev):
    """A subscriber to IntIdRemovedEvent,
    remove assignments for removed object """
    getUtility(IAssignmentsConfiglet).removeAssignmentsFor(object)
