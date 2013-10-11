#----------------------------------------------------------------------
# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

__doc__ = """
Menublock
----------
Element to render navigation trees and linked table of contents. The menublock can be used
as main navigation for the web page.
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase


class menublock(PageElementBase):
    
    def GetMenuPages(self):
        """
        """
        menu = self.data.get("menutype")
        if menu == u"sub":
            return self.GetPage().GetPages(hidden=0)
        elif menu == u"level":
            p = self.GetPage().parent
            if not p:
                #root
                p = self.GetPage()
            return p.GetPages(hidden=0)
        return []


# text type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "menublock",
    name = _(u"Navigation"),
    dbparam = "menublocks",
    context = "nive_cms.menublock.menublock",
    template = "menublock.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/menublock.png",
    description = _(u"Element to render navigation trees and linked table of contents. The menublock can be used as main navigation for the web page.")
)

css =[  {'id': u'cols1_2', 'name': _(u'50 % width left')},
        {'id': u'cols1_3', 'name': _(u'33 % width left')},
        {'id': u'cols2_3', 'name': _(u'66 % width left')},
        {'id': u'colsRight1_2', 'name': _(u'50 % width right')},
        {'id': u'colsRight1_3', 'name': _(u'33 % width right')},
        {'id': u'colsRight2_3', 'name': _(u'66 % width right')},
]
menu=[  {'id': u'sub', 'name': _(u'Sub pages')},
        {'id': u'level', 'name': _(u'Same level pages')},
        {'id': u'tree', 'name': _(u'Tree navigation')},
        {'id': u'subtree', 'name': _(u'Tree navigation - first level as base')},
]
configuration.data = [
    FieldConf(id="cssClass", datatype="list", size=12, default=u"", name=_(u"Styling"), listItems=css, description=u""),
    FieldConf(id="menutype", datatype="list", size=12, default=u"", name=_(u"Menu type"), listItems=menu, description=u"")
]

fields = ["title", "menutype", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.views = []
