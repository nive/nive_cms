# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Editor Root
------------
In edit mode the cms will use this root to render the webpage. nive_cms.root is used
in normal mode. 
"""

from nive.definitions import RootConf, FieldConf
from nive.definitions import implements, IWebsiteRoot, ICMSRoot
from nive.security import Deny, Allow, Everyone

from nive.adminview.view import RootnameValidator

from nive_cms.i18n import _
from nive_cms.baseobjects import PageRootBase


class cmsroot(PageRootBase):

    #implements(IWebsiteRoot, ICMSRoot)
    implements(ICMSRoot)
    extension = u"html"
    
    def Init(self):
        self.__acl__ = (
            (Allow, 'group:editor', 'view'),
            (Allow, 'group:author', 'view'),
            (Allow, 'group:reviewer', 'view'),
            (Allow, 'group:reader', 'view'),
            (Allow, 'group:admin', 'view'),
            (Deny, Everyone, 'view'),
        )




# Root definition ------------------------------------------------------------------
#@nive_module
configuration = RootConf(
    id = "editor",
    context = "nive_cms.cmsview.cmsroot.cmsroot",
    template = "root.pt",
    default = False,
    subtypes = "*",
    name = _(u"Home"),
    extensions = ("nive.extensions.persistentRoot.Persistent",),
    description = __doc__
)

configuration.data = [
    FieldConf(id=u"pool_filename",   datatype="string",      size=30,   required=1,  name=_(u"Root url name"),
              settings={"validator": RootnameValidator}, default=u""),
    FieldConf(id=u"title",           datatype="string",      size=255,  required=0,  name=_(u"Root title"),
              default=configuration.name),
    FieldConf(id=u"description",     datatype="text",        size=5000, required=0,  name=_(u"Root description")),
    FieldConf(id=u"pool_groups",     datatype="checkbox", size=250,  required=0,  name=_(u"Permission"),
              default=u"", description=_(u"Only displayed to users in the selected group"))
]


fields = ["title", "description", "pool_filename", "pool_groups"]
configuration.forms = {"edit": {"fields":fields}}

configuration.toJson = tuple(fields)

configuration.views = []
