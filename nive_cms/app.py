# -*- coding: utf-8 -*-
# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Nive cms default configuration

This file links together all modules included in a default nive installation.

Minimal local system configuration (sqlite example) and usage
------------------------------------------------------
::
    
    from nive.definitions import AppConf, DatabaseConf

    app = AppConf("nive_cms.app",
                  id = "website",
                  title = "My website")
    dbConfiguration = DatabaseConf(
                       fileRoot="/var/opt/website",
                       context=u"Sqlite3",
                       dbName="/var/opt/website/website.db")
    app.modules.append(dbConfiguration)
    design = ViewModuleConf("nive_cms.design.view")
    app.modules.append(design)

- Groups: *group:editor, group:author, group:admin*
- Additional meta fields: *Permission (pool_groups)* Object only displayed to users in 
  the selected group

A design is not included by default. The default can simply be included with the 
following line ::

    app.modules.append("nive_cms.design.view")

To include a customized copy of the design use ::

    design = ViewModuleConf("nive_cms.design.view")
    # design customizations here
    design.static = "mywebsite:static" 
    # add to website
    app.modules.append(design)

This will replace the static directory of the design with your own directory. However, now you will
have to add the required css, images and javascript used by the templates to the new folder.
(For a start just copy the contents of ``nive_cms.design:static``.)
"""
import copy

from nive_cms.i18n import _
from nive.definitions import implements, IWebsite
from nive.definitions import AppConf, FieldConf, GroupConf
from nive.definitions import AllMetaFlds
from nive.security import ALL_PERMISSIONS, Allow, Everyone, Deny
from nive.components.objects.base import ApplicationBase


#@nive_module
configuration = AppConf(
    id = "website",
    title = u"Nive cms",
    context = "nive_cms.app.WebsitePublisher",
    workflowEnabled = True,
    columns=[u"footer"],
)

configuration.meta.append(FieldConf(id="pool_groups", datatype="mcheckboxes", size=250, default="", 
                                    name=_(u"Permission"), 
                                    description=_(u"Only displayed to users in the selected group")))

configuration.modules = [
    # objects
    "nive_cms.box", "nive_cms.column", "nive_cms.menublock", "nive_cms.file", 
    "nive_cms.image", "nive_cms.media", "nive_cms.note", "nive_cms.text",
    "nive_cms.news", "nive_cms.spacer", "nive_cms.link", "nive_cms.code", 
    # page, root
    "nive_cms.root", "nive_cms.page", 
    # cms editor
    "nive_cms.cmsview",
    # design: not included by default
    #"nive_cms.design.view"
    # workflow
    "nive_cms.workflow",
    "nive_cms.workflow.wf.wfProcess", 
    #extensions
    "nive_cms.extensions.fulltextpage", 
    #"nive.components.extensions.localgroups",
    # tools
    "nive.components.tools.dbStructureUpdater", "nive.components.tools.dbSqldataDump", "nive.components.tools.cmsstatistics",
    "nive.components.tools.gcdump",
    # administration and persistence
    "nive.adminview",
    "nive.components.extensions.persistence.dbPersistenceConfiguration"
]

configuration.acl = [
    (Allow, Everyone, 'view'),
    (Allow, 'group:editor', 'read'),
    (Allow, 'group:editor', 'add'),
    (Allow, 'group:editor', 'edit'), 
    (Allow, 'group:editor', 'delete'), 
    (Allow, 'group:editor', 'publish'), 
    (Allow, 'group:editor', 'revoke'), 
    (Allow, 'group:author', 'read'),
    (Allow, 'group:author', 'add'),
    (Allow, 'group:author', 'edit'), 
    (Allow, 'group:author', 'delete'), 
    (Allow, 'group:reviewer', 'read'),
    (Allow, 'group:reviewer', 'publish'),
    (Allow, 'group:reviewer', 'revoke'), 
    (Allow, 'group:reader', 'read'),
    (Allow, 'group:admin', ALL_PERMISSIONS), 
    (Deny, Everyone, ALL_PERMISSIONS),
]

configuration.groups = [ 
    GroupConf(id="group:editor", name="group:editor"),
    GroupConf(id="group:author", name="group:author"),
    GroupConf(id="group:reviewer", name="group:reviewer"),
    GroupConf(id="group:reader", name="group:reader"),
    GroupConf(id="group:admin",  name="group:admin"),
]


class WebsitePublisher(ApplicationBase):
    """ the main cms application class """
    implements(IWebsite)
    
    
