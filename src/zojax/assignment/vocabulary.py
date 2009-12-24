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
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from interfaces import IAssigneesProvider


def AssigneesVocabulary(context, _emptyVoc=SimpleVocabulary(())):
    provider = IAssigneesProvider(context, None)

    if provider is None:
        return _emptyVoc

    getPrincipal = getUtility(IAuthentication).getPrincipal

    terms = []
    for pid in provider.assignees():
        try:
            principal = getPrincipal(pid)
        except PrincipalLookupError:
            continue

        terms.append(
            (principal.title, SimpleTerm(pid, pid, principal.title)))

    terms.sort()

    return SimpleVocabulary([term for _t, term in terms])
