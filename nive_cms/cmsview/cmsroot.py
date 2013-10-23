# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

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
