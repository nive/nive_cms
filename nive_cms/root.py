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
    extensions = ("nive.extensions.persistentRoot.Persistent","nive_cms.extensions.path.PersistentRootPath"),
    name = _(u"Home"),
    description = _(u"The root is the home page of the website. All contained pages and elements are stored in the database.")
)
