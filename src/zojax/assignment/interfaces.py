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
from zope import schema, interface
from zope.component.interfaces import IObjectEvent

ROLE_ID = 'content.Assignee'
NOT_ASSIGNED = '__not_assigned__'


class IAssignmentsAware(interface.Interface):
    """ marker interface for objects that support assignments """


class IAssigneesProvider(interface.Interface):
    """ assignees provider """

    def assignees():
        """ return principal ids """


# assignees field

class IAssigneesField(interface.Interface):
    """ schema field """


# assingments management

class IReadAssignments(interface.Interface):
    """ object assignments, read interface """

    assignees = interface.Attribute('List of all assignees')

    def isAssigned(pid):
        """ check is principal assigned """

    def getAssignees():
        """ return list of assignees (IPrincipal object) """


class IManageAssignments(interface.Interface):
    """ manage object assignments """

    def assign(assignees):
        """ unassign old assigners and assign new """

    def reassign(assignees):
        """ assign principals is not assigned yet """

    def unassign(assignees):
        """ unassign assignees """


class IAssignments(IManageAssignments, IReadAssignments):
    """ assignments management """


# configet

class IAssignmentsConfiglet(interface.Interface):
    """ configlet """

    def getAssignmentsFor(context):
        """ return IAssignments object for context """

    def removeAssignmentsFor(context):
        """ remove IAssignments object for context """


# events

class IAssignEvent(IObjectEvent):
    """ assign to object event """

    principal = interface.Attribute('Principal id')


class IPrincipalAssignedEvent(IAssignEvent):
    """ principal assigned to object event """


class IPrincipalUnassignedEvent(IAssignEvent):
    """ principal unassigned to object event """
