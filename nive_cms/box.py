# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Box
----
A box is a container to group elements on a page. It can be used as an
advanced styling element for web pages. The box itself only stores a title and a css class.
"""

from nive_cms.i18n import _
from nive.definitions import StagPage, StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementContainerBase


class box(PageElementContainerBase):

    @property
    def page(self):
        return self.parent.GetPage()

    def IsContainer(self):
        #
        return True

    def IsPage(self):
        #
        return False
    
    def GetPage(self):
        # return the current element container
        return self.parent.GetPage()

    def GetElementContainer(self):
        # return the current element container
        return self #.parent
    
    def GetContainer(self):
        # return the current element container
        return self.parent




#@nive_module
configuration =  ObjectConf(
    id = "box",
    name = _(u"Box"),
    dbparam = "box",
    context = "nive_cms.box.box",
    template = "box.pt",
    selectTag = StagPageElement,
    subtypes = ("nive.definitions.INonContainer",),
    container = True,
    icon = "nive_cms.cmsview:static/images/types/box.png",
    description = _(u"A box is a container to group elements on a page. It can be used as an" 
                    u"advanced styling element for web pages. The box itself only stores a title and styling selector.")
)

# data definition ------------------------------------------------------------------

configuration.data = [
    FieldConf(id="span", datatype="list", size=20, default=u"", listItems=(), 
              name=_(u"Block size"), description=u""),
    FieldConf(id="spanoffset", datatype="list", size=20, default=u"", listItems=(), 
              name=_(u"Block empty offset left"), description=_(u"Please note: The blocksize and offset values added together can not be larger than 12. Adjust both fields accordingly.")),
    FieldConf(id="highlight", datatype="bool", size=2, default=False,  
              name=_(u"Highlight box contents"), description=_(u"This option will add a colored background to highlight the box and its contents.")),
    FieldConf(id="gallery", datatype="bool", size=2, default=False,  
              name=_(u"Use as image gallery"), description=_(u"Use this setting if you want to add floating image teasers to this box.")),
    FieldConf(id="responsive", datatype="checkbox", size=20, default=u"", listItems=(),
              name=_(u"Enable responsive layout"), description=_(u"Show and hide the box and it contents. The setting takes effect based on viewport or browser window sizes. It does not check the hardware device. Please note: The responsive setting is ignored in edit mode.")),
]


fields = ["title", "span", "spanoffset", "highlight", "gallery", "responsive", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

jsonfields = fields + ["pool_type","pool_filename"]
configuration.toJson = tuple(jsonfields)

configuration.views = []



    
