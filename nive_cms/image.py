# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Image
-----
The image element inserts images into the web page.

Images uploaded as fullsize will be be linked as pop ups.

If the Python Image Library (PIL) is installed automated image conversion on upload can be
activated by adding `nive_cms.extensions.images.ImageProcessor` to configuration.extensions.
::

    ProfileImage = Conf(source="imagefull", dest="image", format="JPEG", 
                        quality="85", width=360, height=0, extension="jpg", 
                        condition=CheckDeafult)

    configuration.imageProfiles = [ProfileImage]

The default image settings for conversions. 
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf, Conf
from nive_cms.baseobjects import PageElementFileBase

from nive_cms.extensions.images import PILloaded

class image(PageElementFileBase):
    """
    """
    # bw 0.9.11
    def Span(self):
        # css class span for the css selection
        if self.data.cssClass=="teaserl":
            return u"span4"
        elif self.data.cssClass=="teasers":
            return u"span2"
        return u"span3"    


# image type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "image",
    name = _(u"Image"),
    dbparam = "images",
    context = "nive_cms.image.image",
    template = "image.pt",
    selectTag = StagPageElement,
    extensions = [],
    icon = "nive_cms.cmsview:static/images/types/image.png",
    description = _(u"The image element inserts images into the web page.")
)

configuration.data = [
    FieldConf(id="image",     datatype="file", size=0,     default=u"", name=_(u"Imagefile")),
    FieldConf(id="imagefull", datatype="file", size=0,     default=u"", name=_(u"Imagefile fullsize")),
    FieldConf(id="textblock", datatype="htext",size=100000,default=u"", name=_(u"Text"), fulltext=1, required=0),
    FieldConf(id="cssClass",  datatype="list", size=10,    default=u"", name=_(u"Styling"), listItems=()),
    FieldConf(id="link",      datatype="url",  size=1000,  default=u"", name=_(u"Link"))
]

if PILloaded and "nive_cms.extensions.images.ImageProcessor" in configuration.extensions:
    fields = ["title", "imagefull", "textblock", "cssClass", "link", "pool_groups"]
else:
    fields = ["title", "image", "imagefull", "textblock", "cssClass", "link", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.toJson = ("title", "image", "imagefull", "textblock", "cssClass", "link", "pool_groups", "pool_type", "pool_filename")

configuration.views = []


ProfileImage = Conf(source="imagefull", dest="image", format="JPEG", quality="90", width=360, height=0, extension="jpg")

configuration.imageProfiles = [ProfileImage]


