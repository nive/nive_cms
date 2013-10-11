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
Root
----
The *root* is the home page of the website. All contained pages and elements are stored 
in the database. The root itself does not store anything in the database.

Also this object provides search functions and sql query wrappers.
"""

from nive_cms.i18n import _
from nive_cms.baseobjects import PageRootBase
from nive.definitions import IWebsiteRoot, implements
from nive.definitions import RootConf


class root(PageRootBase):

    implements(IWebsiteRoot)
    extension = u"html"
    
    def Init(self):
        self.queryRestraints = {"pool_state": 1}, {}
    
    


# Root definition ------------------------------------------------------------------
#@nive_module
configuration = RootConf(
    id = "root",
    context = "nive_cms.root.root",
    template = "root.pt",
    default = True,
    subtypes = "*",
    extensions = ("nive.components.extensions.persistentRoot.Persistent",),
    name = _(u"Home"),
    description = _(u"The root is the home page of the website. All contained pages and elements are stored in the database.")
)
