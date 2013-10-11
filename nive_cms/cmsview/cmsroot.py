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
Editor Root
------------
In edit mode the cms will use this root to render the webpage. nive_cms.root is used
in normal mode. 
"""

from nive_cms.i18n import _
from nive.definitions import RootConf, implements, IWebsiteRoot, ICMSRoot
from nive_cms.baseobjects import PageRootBase


class cmsroot(PageRootBase):

    #implements(IWebsiteRoot, ICMSRoot)
    implements(ICMSRoot)
    extension = u"html"
    
    


# Root definition ------------------------------------------------------------------
#@nive_module
configuration = RootConf(
    id = "editor",
    context = "nive_cms.cmsview.cmsroot.cmsroot",
    template = "root.pt",
    default = False,
    subtypes = "*",
    name = _(u"Home"),
    extensions = ("nive.components.extensions.persistentRoot.Persistent",),
    description = __doc__
)
