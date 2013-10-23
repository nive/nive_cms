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
        return self.parent

    def GetResponsiveClass(self, editmode=False):
        """
        Returns the responsive class to be attached to the box.
        In edit mode all boxes are visible and the data.responsive setting
        is prefixed with `pe_`. (e.g. pe_visible-tablet pe_visible-phone)
        
        To make boxes always accessible in edit mode the responsive setting is
        disabled and boxes are highlighted appropriately.
        """
        r = self.data.responsive
        if isinstance(r, basestring):
            r=r.split(u", ")
        if not editmode or not r:
            return u" ".join(r)
        return u" ".join([u"pe_"+c for c in r])


    def IsContainer(self):
        #
        return True

    def IsPage(self):
        #
        return False
    
    def GetPage(self):
        # return the current element container
        return self.parent

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
    container = True,
    icon = "nive_cms.cmsview:static/images/types/box.png",
    description = _(u"A box is a container to group elements on a page. It can be used as an" 
                    u"advanced styling element for web pages. The box itself only stores a title and styling selector.")
)

# data definition ------------------------------------------------------------------
css =[  {'id': u'span1', 'name': _(u'Span 1')},
        {'id': u'span2', 'name': _(u'Span 2')},
        {'id': u'span3', 'name': _(u'Span 3')},
        {'id': u'span4', 'name': _(u'Span 4')},
        {'id': u'span5', 'name': _(u'Span 5')},
        {'id': u'span6', 'name': _(u'Span 6')},
        {'id': u'span7', 'name': _(u'Span 7')},
        {'id': u'span8', 'name': _(u'Span 8')},
        {'id': u'span9', 'name': _(u'Span 9')},
        {'id': u'span10', 'name': _(u'Span 10')},
        {'id': u'span11', 'name': _(u'Span 11')},
        {'id': u'span12', 'name': _(u'Span 12 (100% width)')},
        {'id': u'hero-unit', 'name': _(u'Top box (hero-unit)')},
]
off =[  {'id': u'', 'name': _(u'none')},
        {'id': u'offset1', 'name': _(u'Offset 1')},
        {'id': u'offset2', 'name': _(u'Offset 2')},
        {'id': u'offset3', 'name': _(u'Offset 3')},
        {'id': u'offset4', 'name': _(u'Offset 4')},
        {'id': u'offset5', 'name': _(u'Offset 5')},
        {'id': u'offset6', 'name': _(u'Offset 6')},
        {'id': u'offset7', 'name': _(u'Offset 7')},
        {'id': u'offset8', 'name': _(u'Offset 8')},
        {'id': u'offset9', 'name': _(u'Offset 9')},
        {'id': u'offset10', 'name': _(u'Offset 10')},
        {'id': u'offset11', 'name': _(u'Offset 11')},
]        
resp =[ {'id': u'visible-desktop', 'name': _(u'Visible in desktop viewports')},
        {'id': u'visible-tablet', 'name': _(u'Visible in tablet viewports')},
        {'id': u'visible-phone', 'name': _(u'Visible in phone viewports')},
]        

configuration.data = [
    FieldConf(id="span", datatype="list", size=20, default=u"", listItems=css, 
              name=_(u"Block size"), description=u""),
    FieldConf(id="spanoffset", datatype="list", size=20, default=u"", listItems=off, 
              name=_(u"Block empty offset left"), description=_(u"Please note: The blocksize and offset values added together can not be larger than 1. Adjust both fields accordingly.")),
    FieldConf(id="highlight", datatype="bool", size=2, default=False,  
              name=_(u"Highlight box contents"), description=_(u"This option will add a colored background to highlight the box and its contents.")),
    FieldConf(id="gallery", datatype="bool", size=2, default=False,  
              name=_(u"Use as image gallery"), description=_(u"Use this setting if you want to add floating image teasers to this box.")),
    FieldConf(id="responsive", datatype="mcheckboxes", size=20, default=u"", listItems=resp, 
              name=_(u"Enable responsive layout"), description=_(u"Show and hide the box and it contents. The setting takes effect based on viewport or browser window sizes. It does not check the hardware device. Please note: The responsive setting is ignored in edit mode.")),
]    


fields = ["title", "span", "spanoffset", "highlight", "gallery", "responsive", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.views = []



    
