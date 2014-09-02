# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Code
-----
Text element to add code snippets to web pages. Supports Javascript, raw HTML and CSS. 
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase


class code(PageElementBase):
    """
    """
    



# text type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "code",
    name = _(u"Code"),
    dbparam = "codes",
    context = "nive_cms.codeblock.code",
    template = "code.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/code.png",
    description = _(u"Text element to add code snippets to web pages. Supports Javascript, HTML and CSS.")
)

ct =[ {'id': u'raw', 'name': _(u'No format')},
      {'id': u'js', 'name': _(u'Javascript')},
      {'id': u'html', 'name': _(u'HTML')},
      {'id': u'css', 'name': _(u'CSS')},
]

configuration.data = [
    FieldConf(id="codetype",  datatype="list", size=10, default="raw", name=_(u"Type"), listItems=ct, fulltext=False, description=u""),
    FieldConf(id="codeblock", datatype="code", size=50000, default="", name=_(u"Code"), fulltext=False, description=u""),
]

fields = ["title","codeblock", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
