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
from persistent import Persistent
from BTrees.OOBTree import OOTreeSet

from zope import event, interface, component
from zope.location import Location
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from events import PrincipalAssignedEvent, PrincipalUnassignedEvent
from interfaces import IAssignments, IAssignmentsAware, IAssignmentsConfiglet


class Assignments(Persistent, Location):
    interface.implements(IAssignments)

    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.assignees = OOTreeSet()

    def assign(self, principals):
        modified = False
        context = getUtility(IIntIds).getObject(self.doc_id)

        for pid in tuple(self.assignees):
            if pid not in principals:
                self.assignees.remove(pid)
                event.notify(PrincipalUnassignedEvent(context, pid))

        for pid in principals:
            if pid not in self.assignees:
                self.assignees.insert(pid)
                event.notify(PrincipalAssignedEvent(context, pid))

    def reassign(self, principals):
        modified = False
        context = getUtility(IIntIds).getObject(self.doc_id)

        for pid in principals:
            if pid not in self.assignees:
                self.assignees.insert(pid)
                event.notify(PrincipalAssignedEvent(context, pid))

    def unassign(self, principals):
        context = getUtility(IIntIds).getObject(self.doc_id)

        for principal in principals:
            if principal in self.assignees:
                self.assignees.remove(principal)
                event.notify(PrincipalUnassignedEvent(context, principal))

    def getAssignees(self):
        getPrincipal = getUtility(IAuthentication).getPrincipal

        assignees = []
        for pid in self.assignees:
            try:
                assignees.append(getPrincipal(pid))
            except PrincipalLookupError:
                pass

        return assignees

    def isAssigned(self, pid):
        return pid in self.assignees


@component.adapter(IAssignmentsAware)
@interface.implementer(IAssignments)
def getAssignments(context):
    return getUtility(IAssignmentsConfiglet).getAssignmentsFor(context)
