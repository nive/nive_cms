# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
File
----
The *file* element provides a simple file download with title and optional description.
"""

from nive_cms.i18n import _
from nive.utils.utils import FormatBytesForDisplay

from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementFileBase


class file(PageElementFileBase):
    
    def GetDownloadTitle(self):
        # title with type and size
        title = self.meta["title"]
        f = self.files.get("file")
        if not f:
            return title
        t = f["extension"]
        s = f["size"]
        if s:
            s = FormatBytesForDisplay(s)
        return u"%s (%s %s)" % (title, t, s)
    
     
    def Init(self):
        self.ListenEvent("commit", "FilenameToTitle")

    def FilenameToTitle(self, **kw):
        if self.files.get("file") and not self.meta["title"]:
            self.meta["title"] = self.files.get("file")["filename"]
        


# file type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "file",
    name = _(u"File"),
    dbparam = "files",
    context = "nive_cms.file.file",
    template = "file.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/file.png",
    description = _(u"The file element provides a simple file download with title and optional description.")
)

configuration.data = [
    FieldConf(id="file",       datatype="file",  size=0,     default=u"", fulltext=1, name=_(u"File"), description=u""),
    FieldConf(id="textblock",  datatype="htext", size=10000, default=u"", name=_(u"Description"), fulltext=1, description=u"")
]

fields = ["title", "file", "textblock", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []



    
