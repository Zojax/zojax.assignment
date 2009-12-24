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
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.traversing.browser import absoluteURL
from zope.app.intid.interfaces import IIntIds

from zojax.table.table import Table
from zojax.table.column import Column

from interfaces import IAssignmentsConfiglet


class Assignments(Table):
    component.adapts(IAssignmentsConfiglet,
                     interface.Interface, interface.Interface)

    pageSize = 30
    enabledColumns = ('id', 'object', 'principals')
    msgEmptyTable = 'There are no assignments.'

    def initDataset(self):
        self.dataset = removeAllProxies(self.context).data.values()


class IdColumn(Column):
    component.adapts(interface.Interface, interface.Interface, Assignments)

    name = 'id'
    title = u'Id'

    def query(self, default=None):
        return self.content.doc_id


class ObjectColumn(Column):
    component.adapts(interface.Interface, interface.Interface, Assignments)

    name = 'object'
    title = u'Object'

    def query(self, default=None):
        return getUtility(IIntIds).queryObject(self.content.doc_id)

    def render(self):
        object = self.query()
        if object is not None:
            return '<a href="%s/">%s</a>'%(
                absoluteURL(object, self.request),
                getattr(object, 'title', object.__name__) or object.__name__)
        else:
            return u'Unknown'


class PrincipalsColumn(Column):
    component.adapts(interface.Interface, interface.Interface, Assignments)

    name = 'principals'
    title = u'Principals'

    def query(self, default=None):
        return self.content.getAssignees()

    def render(self):
        return u', '.join([p.title for p in self.query()])
