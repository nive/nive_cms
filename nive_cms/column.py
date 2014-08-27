# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

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
        return self.meta.pool_unitref == page.id
    
    def GetName(self):
        return self.meta["title"]
    
    def IsContainer(self):
        return True

    def IsPage(self):
        return False

    def GetPage(self):
        return self.parent

    def GetPages(self):
        return []

    def GetElementContainer(self):
        return self 

    def GetContainer(self):
        return self.parent

    def GetColumn(self, name):
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

configuration.toJson = ("title", "showsub", "pool_groups", "pool_type", "pool_filename")

configuration.views = []


    
    
