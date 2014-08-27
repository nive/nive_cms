# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Spacer
------
Styling element to add line breaks and vertical space between elements. 
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase


class spacer(PageElementBase):
    pass
    


# type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "spacer",
    name = _(u"Spacer"),
    dbparam = "spacers",
    context = "nive_cms.spacer.spacer",
    template = "spacer.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/spacer.png",
    description = _(u"Styling element to add line breaks and vertical space between elements.")
)

configuration.data = [
    FieldConf(id="cssClass", datatype="list", size=5, default=u"", listItems=(), name=_(u"Styling"), description=u"")
]

fields =["cssClass", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
