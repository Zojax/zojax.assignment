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
from z3c.form.interfaces import NOVALUE
from z3c.form.datamanager import AttributeField

from interfaces import IAssigneesField


class AssigneesField(AttributeField):
    component.adapts(interface.Interface, IAssigneesField)

    def get(self):
        return self.field.get(self.context)

    def query(self, default=NOVALUE):
        return self.field.query(self.context, default)

    def set(self, value):
        return self.field.set(self.context, value)
