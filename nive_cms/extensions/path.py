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

import string
import unicodedata
import re

from nive.definitions import StagPage, StagPageElement

        
class AlternatePath(object):
    """
    Enables readable url path names instead of ids for object traversal.
    Names are stored as meta.pool_filename and generated from
    title by default. Automatic generation can be disabled by setting
    *meta.customfilename* to False for each object.
    
    Extensions like *.html* are not stored. Path matching works independent 
    from extensions.
    """
    maxlength = 50
    
    def Init(self):
        if self.id == 0:
            # skip roots
            return
        self.ListenEvent("commit", "TitleToFilename")
        self._SetName()

    
    def TitleToFilename(self, **kw):
        """
        Uses title for filename
        """
        customfilename = self.data.get("customfilename",False)
        if customfilename:
            self._SetName()
            return
        # create url compatible filename from title
        filename = self.EscapeFilename(self.meta["title"])
        # make unique filename
        if filename == self.meta["pool_filename"]:
            # no change
            return
        filename = self.UniqueFilename(filename)
        if filename:
            # update
            self.meta["pool_filename"] = filename
            self._SetName()
            return 
        # reset filename
        self.meta["pool_filename"] = u""
        self._SetName()
        
        
    def UniqueFilename(self, name):
        """
        Converts name to valid path/url
        """
        cnt = 1
        root = self.dataroot
        if name == u"file":
            name = u"file_"
        while root.FilenameToID(name, self.parent.id, parameter={u"id":self.id}, operators={u"id":u"!="}) != 0:
            if cnt>1:
                name = name[:-1]+str(cnt)
            else:
                name = name+str(cnt)
            cnt += 1
        return name


    def EscapeFilename(self, path):
        """
        Converts name to valid path/url
        
        Path length between *self.maxlength-20* and *self.maxlength* chars. Tries to cut longer names at spaces.      
        (based on django's slugify)
        """
        if not isinstance(path, unicode):
            path = unicode(path, self.app.configuration.frontendCodepage)
        path = unicodedata.normalize(u'NFKD', path).encode(u'ascii', 'ignore')
        path = unicode(re.sub(u'[^\w\s-]', u'', path).strip().lower())
        path = unicode(re.sub(u'[-\s]+', u'_', path))
        
        # cut long filenames
        cutlen = 20
        if len(path) <= self.maxlength:
            return path
        # cut at '_' 
        pos = path[self.maxlength-cutlen:].find(u"_")
        if pos > cutlen:
            # no '_' found. cut at maxlength.
            return path[:self.maxlength]
        return path[:self.maxlength-cutlen+pos]

    
    # system functions -----------------------------------------------------------------
    
    def __getitem__(self, id):
        """
        Traversal lookup based on object.pool_filename and object.id. Trailing extensions 
        are ignored.
        `file` is a reserved name and used in the current object to map file downloads. 
        """
        if id == u"file":
            raise KeyError, id
        id = id.split(u".")
        if len(id)>2:
            id = (u".").join(id[:-1])
        else:
            id = id[0]
        try:
            id = long(id)
        except:
            name = id
            id = 0
            if name:
                id = self.dataroot.FilenameToID(name, self.id)
            if not id:
                raise KeyError, id
        o = self.GetObj(id)
        if not o:
            raise KeyError, id
        return o

    def _SetName(self):
        self.__name__ = self.meta["pool_filename"]
        if not self.__name__:
            self.__name__ = str(self.id)

    