# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

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
    
    def GetMenuPages(self, **kw):
        """
        """
        menu = self.data.get("menutype")
        if menu == u"sub":
            return self.GetPage().GetPages(hidden=0, **kw)
        elif menu == u"level":
            p = self.GetPage().parent
            if not p:
                #root
                p = self.GetPage()
            return p.GetPages(hidden=0, **kw)
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

menu=[  {'id': u'sub', 'name': _(u'Sub pages')},
        {'id': u'level', 'name': _(u'Same level pages')},
        {'id': u'tree', 'name': _(u'Tree navigation')},
        {'id': u'subtree', 'name': _(u'Tree navigation - first level as base')},
]
configuration.data = [
    FieldConf(id="menutype", datatype="list", size=12, default=u"", name=_(u"Menu type"), listItems=menu, description=u"")
]

fields = ["title", "menutype", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
