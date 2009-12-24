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
from zope.securitypolicy.interfaces import Allow, Unset, IPrincipalRoleMap

from interfaces import ROLE_ID, IAssignments, IAssignmentsAware


class AssigneeRole(object):
    component.adapts(IAssignmentsAware)
    interface.implements(IPrincipalRoleMap)

    def __init__(self, context):
        self.assignees = IAssignments(context).assignees

    def getPrincipalsForRole(self, role_id):
        if role_id == ROLE_ID:
            return ((pid, Allow) for pid in self.assignees)
        else:
            return ()

    def getRolesForPrincipal(self, principal_id):
        if principal_id in self.assignees:
            return ((ROLE_ID, Allow),)
        else:
            return ()

    def getSetting(self, role_id, principal_id):
        if (role_id == ROLE_ID) and (principal_id in self.assignees):
            return Allow
        return Unset

    def getPrincipalsAndRoles(self):
        pass
