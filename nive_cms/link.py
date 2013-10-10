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
Link
-----
With the link element you can add internal or external links into the web page.

Internal links can be referenced as page id (the number) and are resolved automatically.
"""

from nive.i18n import _
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
styles =  [
    {"id": u"", "name": _(u"none")}, 
    {"id": u"btn", "name": _(u"Simple button")}, 
    {"id": u"btn btn-large", "name": _(u"Large button")}, 
    {"id": u"btn btn-small", "name": _(u"Small button")}, 
]
colors =  [
    {"id": u"", "name": _(u"none")}, 
    {"id": u"btn-primary", "name": _(u"Primary")}, 
    {"id": u"btn-info", "name": _(u"Info")}, 
    {"id": u"btn-success", "name": _(u"Success")}, 
    {"id": u"btn-warning", "name": _(u"Warning")}, 
    {"id": u"btn-danger", "name": _(u"Danger")}, 
    {"id": u"btn-inverse", "name": _(u"Inverse")}, 
]
configuration.data = [
    FieldConf(id="linkurl", datatype="url", size=255, default=u"", name=_(u"Link url"), description=_(u"External links must start with http:// or similar. Internal links can be referenced as page id (the number) and are resolved automatically.")),
    FieldConf(id="target",  datatype="list",size=15,  default=u"", listItems=targets, name=_(u"Target window"), description=u""),
    FieldConf(id="style",   datatype="list",size=20,  default=u"", listItems=styles,  name=_(u"Link style"), description=u""),
    FieldConf(id="color",   datatype="list",size=20,  default=u"", listItems=colors,  name=_(u"Button color"), description=u"")
]

fields = ["title", "linkurl", "target", "style", "color", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.views = []
