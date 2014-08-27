# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Link
-----
With the link element you can add internal or external links into the web page.

Internal links can be referenced as page id (the number) and are resolved automatically.
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase


class link(PageElementBase):
    pass


# text type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "link",
    name = _(u"Link"),
    dbparam = "links",
    context = "nive_cms.link.link",
    template = "link.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/link.png",
    description = _(u"With the link element you can add internal or external links into the web page.")
)

targets = [{"id": u"", "name": _(u"Same window")}, {"id": u"blank_", "name": _(u"New window")} ]

configuration.data = [
    FieldConf(id="linkurl", datatype="url", size=255, default=u"", name=_(u"Link url"), description=_(u"External links must start with http:// or similar. Internal links can be referenced as page id (the number) and are resolved automatically.")),
    FieldConf(id="target",  datatype="list",size=15,  default=u"", listItems=targets, name=_(u"Target window"), description=u""),
    FieldConf(id="style",   datatype="list",size=20,  default=u"", listItems=(),  name=_(u"Link style"), description=u""),
    FieldConf(id="color",   datatype="list",size=20,  default=u"", listItems=(),  name=_(u"Button color"), description=u"")
]

fields = ["title", "linkurl", "target", "style", "color", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
