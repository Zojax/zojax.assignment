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
from zope.component.interfaces import ObjectEvent
from interfaces import IPrincipalAssignedEvent, IPrincipalUnassignedEvent


class AssignEvent(ObjectEvent):

    def __init__(self, object, principal):
        super(AssignEvent, self).__init__(object)

        self.principal = principal


class PrincipalAssignedEvent(AssignEvent):
    interface.implements(IPrincipalAssignedEvent)


class PrincipalUnassignedEvent(AssignEvent):
    interface.implements(IPrincipalUnassignedEvent)
