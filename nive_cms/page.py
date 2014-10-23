# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Page
----
Pages are rendered as html files and make up the website.

Optionally pages can

- be hidden in navigation
- have a header displayed in the content area
- have a automatically generated readable url name
- have a manually entered readable url name
"""

from nive_cms.i18n import _

from nive.definitions import StagPage, ObjectConf, FieldConf
from nive_cms.baseobjects import PageBase


class page(PageBase):

    extension = u"html"

    def IsLinked(self):
        """
        returns True if the page is redirected in public mode. 
        """
        return self.data["pagelink"]

    def IsPage(self):
        return True
    

# type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "page",
    name = _(u"Page"),
    dbparam = "pages",
    context = "nive_cms.page.page",
    template = "page.pt",
    selectTag = StagPage,
    container = True,
    workflowEnabled = True,
    icon = "nive_cms.cmsview:static/images/types/page.png",
    description = _(u"Pages are rendered as html files and make up the website.")
)

configuration.data = [
    FieldConf(id="header", datatype="string", size=255, default=u"", fulltext=1, 
              name=_(u"Page header"), description=_(u"Text shown at top of the page")),
    FieldConf(id="titleImage", datatype="file", size=0, default=u"", 
              name=_(u"Title image"), description=""),
    FieldConf(id="description",datatype="text", size=500, default=u"", fulltext=1, 
              name=_(u"Description"), description=_(u"Description used in meta tag for search engines etc.")),
    FieldConf(id="keywords",     datatype="text", size=500, default=u"", fulltext=1, 
              name=_(u"Keywords"), description=_(u"Keywords used in meta tag (not really used by search engines).")),
    
    FieldConf(id="navHidden", datatype="bool", size=1, default=0, 
              name=_(u"Hide in navigation"), description=_(u"Hide the page in navigation. It will only be accessible by direct links.")),
    FieldConf(id="navMenu",    datatype="bool", size=1, default=0, 
              name=_(u"Page is a menu"), description=_(u"Used in some navigation lists. If checked the page is handled as menu.")),
    FieldConf(id="pagelink", datatype="string", size=255, default=u"", 
              name=_(u"Page is redirected to this link"), description=_(u"Automatically redirect the page to the linked page. Only in view mode.")),
    FieldConf(id="customfilename", datatype="bool", size=1, default=0, 
              name=_(u"Enter page filename manually"), description=_(u"By default page URL-names are generated automatically by the title. Use this option to change the default behaviour.")),
]

fields = ["title", "header", "description", "navHidden", "pagelink", 
          "customfilename", "pool_filename", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
