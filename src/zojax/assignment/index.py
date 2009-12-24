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
from zojax.catalog.utils import Indexable
from zc.catalog.catalogindex import SetIndex

from interfaces import NOT_ASSIGNED, IAssignments


def assignmentsIndex():
    return SetIndex(
        'assignees', Indexable('zojax.assignment.index.IndexableAssignments'))


class IndexableAssignments(object):

    def __init__(self, context, default=None):
        assignments = IAssignments(context, None)

        if assignments is None:
            self.assignees = default
        else:
            assignees = assignments.assignees
            if not assignees:
                assignees = (NOT_ASSIGNED,)

            self.assignees = tuple(assignees)
