# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Text
-----
Text element for the web page. Can be used to add headers, preformatted text
and paragraphs to the web page. 
"""

from nive_cms.i18n import _
from nive.utils.utils import ConvertHTMLToText, CutText

from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase


class text(PageElementBase):
    """
    basic text class
    """
    
    titleLen = 20

    def Init(self):
        self.ListenEvent("commit", "TextToTitle")


    def TextToTitle(self, **kw):
        text = ConvertHTMLToText(self.data.get("textblock"), removeReST=True)
        self.meta["title"] = CutText(text, self.titleLen, postfix=u"")
        return True


# text type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "text",
    name = _(u"Text"),
    dbparam = "texts",
    context = "nive_cms.text.text",
    template = "text.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/text.png",
    description = _(u"Text element for the web page. Can be used to add headers, preformatted text and paragraphs to the web page. ")
)

configuration.data = [
    FieldConf(id="textblock", datatype="htext", size=100000, default=u"", name=_(u"Text"), fulltext=True, description=u""),
]

fields = ["textblock", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
