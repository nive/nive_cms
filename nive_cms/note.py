# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Note
----
Simple text note for authors. The note is only visible to cms authors and not published.
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementBase
from nive.utils.utils import ConvertHTMLToText, CutText

class note(PageElementBase):

    titleLen = 20

    def Init(self):
        self.ListenEvent("commit", "TextToTitle")

    def TextToTitle(self, **kw):
        text = ConvertHTMLToText(self.data.get("textblock"), removeReST=True)
        self.meta["title"] = CutText(text, self.titleLen, postfix=u"")
        return True
    


# note type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "note",
    name = _(u"Note"),
    dbparam = "notes",
    context = "nive_cms.note.note",
    template = "note.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/note.png",
    description = _(u"Simple text note for authors. The note is only visible to cms authors and not published.")
)

configuration.data = [
    FieldConf(id="textblock", datatype="htext", size=50000, default=u"", name=_(u"Note"), description=u"")
]

fields = ["textblock", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []
