# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
News item
---------
Simple news item with title, text, image, publish date and link.
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase


class news(PageElementBase):
    pass


# news type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "news",
    name = _(u"News"),
    dbparam = "news",
    context = "nive_cms.news.news",
    template = "news.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/news.png",
    description = _(u"Simple news item with title, text, image, publish date and link.")
)

configuration.data = [
    FieldConf(id="image",     datatype="file",  size=0,      default=u"", name=_(u"Imagefile"), description=u""),
    FieldConf(id="textblock", datatype="htext", size=100000, default=u"", fulltext=1, name=_(u"Text"), description=u""),
    FieldConf(id="publish",   datatype="date",  size=0,      default=u"", required=0, name=_(u"Date"), description=_(u"Used as publish date on the website.")),
    FieldConf(id="cssClass",  datatype="list",  size=10,     default=u"", listItems=(), name=_(u"Styling"), description=u""),
    FieldConf(id="link",      datatype="url",   size=1000,   default=u"", name=_(u"Link"), description=u"")
]

fields = ["title", "textblock", "image", "publish", "link", "cssClass", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []

