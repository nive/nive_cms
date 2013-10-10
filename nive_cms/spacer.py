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
Spacer
------
Styling element to add line breaks and vertical space between elements. 
"""

from nive.i18n import _
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

css =[  {'id': u'bo', 'name': _(u'Border')},
        {'id': u'h0', 'name': _(u'Invisible')},
        {'id': u'h1', 'name': _(u'1 line')},
        {'id': u'h2', 'name': _(u'2 lines')},
        {'id': u'h3', 'name': _(u'3 lines')},
        {'id': u'h4', 'name': _(u'4 lines')},
        ]

configuration.data = [
    FieldConf(id="cssClass", datatype="list", size=5, default=u"", listItems=css, name=_(u"Styling"), description=u"")
]

fields =["cssClass", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.views = []
