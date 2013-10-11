#----------------------------------------------------------------------
# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

__doc__ = """
Media
-----
Element to insert audio or video files into the web page. Uses HTML 5 media and audio tags
and the browser's default player.
"""

from nive_cms.i18n import _
from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive_cms.baseobjects import PageElementFileBase


class media(PageElementFileBase):
    
    def IsVideo(self):
        return self.data.get("player")==u"video"

    def IsAudio(self):
        return self.data.get("player")==u"audio"
    


# media type definition ------------------------------------------------------------------
#@nive_module
configuration = ObjectConf(
    id = "media",
    name = _(u"Media"),
    dbparam = "mediafile",
    context = "nive_cms.media.media",
    template = "media.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/media.png",
    description = _(u"Element to insert audio or video files into the web page. Uses HTML 5 media" 
                    u"and audio tags and the browser's default player.")
)

player = [{"id": u"video", "name": _(u"Video player")}, 
          {"id": u"audio", "name": _(u"Audio player")}]

configuration.data = [
    FieldConf(id="media", datatype="file", size=0, default=u"", name=_(u"Mediafile"), description=u""),
    FieldConf(id="mediaalt", datatype="file", size=0, default=u"", 
              name=_(u"Alternative format"), description=_(u"To support all browsers you need to provide two different file formats.")),
    FieldConf(id="player", datatype="list", size=10, listItems=player, default=u"", name=_(u"Player"), description=u""),
    FieldConf(id="textblock", datatype="htext", size=10000, default=u"", fulltext=1, name=_(u"Text"), description=u"")
]

fields = ["title", "media", "mediaalt", "player", "textblock", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.views = []
