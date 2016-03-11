# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

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
from nive.definitions import RootConf, FieldConf

from nive.adminview.view import RootnameValidator



class root(PageRootBase):

    implements(IWebsiteRoot)
    extension = u"html"
    
    def Init(self):
        self.queryRestraints = {"pool_state": 1}, {}
    
    


# Root definition ------------------------------------------------------------------
#@nive_module
configuration = RootConf(
    id = "content",
    context = "nive_cms.root.root",
    template = "root.pt",
    default = True,
    subtypes = "*",
    extensions = ("nive.extensions.persistentRoot.Persistent",),
    name = _(u"Home"),
    description = _(u"The root is the home page of the website. All contained pages and elements are stored in the database.")
)

# Disabled "nive_cms.extensions.path.PersistentRootPath"

configuration.data = [
    FieldConf(id=u"description",     datatype="text",        size=5000, required=0,  name=_(u"Root description")),
]

fields = ["title",
          "description",
          #FieldConf(id=u"pool_filename",   datatype="string",      size=30,   required=1,  name=_(u"Root url name"),
          #          settings={"validator": RootnameValidator}, default=u""),
          "pool_groups"]
configuration.forms = {"edit": {"fields":fields}}

configuration.toJson = tuple(fields)

