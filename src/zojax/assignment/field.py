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
from zope.schema import Tuple, Choice
from zope.schema.interfaces import ConstraintNotSatisfied
from zope.schema.fieldproperty import FieldProperty

from interfaces import IAssigneesField, IAssignments, IAssigneesProvider


class AssigneesField(Tuple):
    interface.implements(IAssigneesField)

    def __init__(self, *args, **kw):
        kw['value_type'] = Choice(vocabulary = 'assignments.assignees')

        super(AssigneesField, self).__init__(*args, **kw)

    def get(self, object):
        assignments = IAssignments(object, None)
        if assignments is not None:
            return tuple(assignments.assignees)
        return ()

    def query(self, object, default=None):
        assignments = IAssignments(object, None)
        if assignments is not None:
            return tuple(assignments.assignees)
        return default

    def set(self, object, value):
        if self.readonly:
            raise TypeError("Can't set values on read-only fields.")

        assignments = IAssignments(object, None)
        if assignments is not None:
            assignments.assign(value)
        else:
            raise TypeError("Object does not implements IAssignments interface.")
