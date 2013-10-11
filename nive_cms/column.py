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
Column
------
A column is a container to group elements on a page. Columns are not added like
normal page elements but have to be defined manually in the main template. A column can
be inherited through a hierarchy of pages.
"""

from nive_cms.i18n import _
from nive.definitions import StagPage, StagPageElement, ObjectConf, FieldConf, IColumn, implements
from nive_cms.baseobjects import PageElementContainerBase


class column(PageElementContainerBase):
    implements(IColumn)
    
    @property
    def page(self):
        return self.parent

    def IsLocal(self, page):
        #
        return self.meta.pool_unitref == page.id
    
    def GetName(self):
        #
        return self.meta["title"]
    
    def IsContainer(self):
        #
        return True

    def IsPage(self):
        #
        return False

    def GetPage(self):
        # returns the current page
        return self.parent

    def GetPages(self):
        # columns have no subpages
        return []

    def GetElementContainer(self):
        # returns the current element container
        return self 

    def GetContainer(self):
        # returns the current container
        return self.parent

    def GetColumn(self, name):
        # 
        if name == self.meta["title"]:
            return self
        return self.GetPage().GetColumn(name)


# type definition ------------------------------------------------------------------
#@nive_module
configuration =  ObjectConf(
    id = "column",
    name = _(u"Column"),
    dbparam = "columnbox",
    context = "nive_cms.column.column",
    template = "column.pt",
    hidden = True,
    selectTag = StagPageElement,
    container = True,
    icon = "nive_cms.cmsview:static/images/types/column.png",
    description = _(u"A column is a container to group elements on a page. Columns are not added like"
                    u"normal page elements but have to be defined manually in the main template. A column can"
                    u"be inherited through a hierarchy of pages.")
)
configuration.data = [
    FieldConf(id="showsub", datatype="bool", size=2, default=1, name=_(u"Show on subpages"), description=_(u"If checked the column will be displayed on sub pages until overwritten."))
]

configuration.forms = {
        "create": {"fields": [FieldConf(id="title", datatype="string", size=10, default=u"", hidden=1, required=1, name=_(u"Column type")),
                              "showsub", "pool_groups"]},
        "edit":   {"fields": ["showsub", "pool_groups"]}
}

configuration.views = []


    
    
