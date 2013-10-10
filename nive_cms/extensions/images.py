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
Image processing extension
--------------------------
Converts images based on profiles and stores the converted images as different
files in object.
Profiles are configured as ``object.configuration.imageProfiles`` with the following attributes: ::

    source = "imagefull": field id of the source image 
    dest = "image": field id of the destination image
    format = "jpg": image format
    quality = "80": quality depending on format
    width = 400: width of new image
    height = 0: height of new image
    extension = "jpg" : file name extension
    condition = None : callback function which takes the image object as parameter and returns whether
                       the profile is valid for the image object or not 

Examples ::

    ProfileImage = Conf(source="imagefull", dest="image", format="JPEG", 
                        quality="80", width=400, height=0, extension="jpg")
    ProfileIcon =  Conf(source="imagefull", dest="icon",  format="JPEG", 
                        quality="70", width=100, height=0, extension="jpg")
    
If either width or height is 0 the new image is scaled proportionally.
See PIL documentation for possible format and quality values.
 
"""

from nive.definitions import Conf
from nive.utils.path import DvPath
from nive.utils.dataPool2.files import File
from nive.helper import ResolveName
from nive.i18n import _

import sys
from time import time

try:     from cStringIO import StringIO
except:  from StringIO import StringIO

try:     from win32pipe import popen
except:  from os import popen

PILloaded = 1
try:     from PIL import Image
except:  PILloaded=0


class ImageProcessor(object):

    def GetImgSize(self, image):
        """
        Returns the image size (width, height) in pixel
        """
        i = self.files.get(image)
        if not i:
            return 0,0
        try:
            im = Image.open(i.path)
            return im.size
        except:
            return 0,0        
        

    def Process(self, images=None, profiles=None):
        """
        Process images and create versions from profiles. ::
        
            images = list of image field ids to process. if none all images based on 
                     selected profiles are processed.
            profiles = list of profiles to process. if none all profiles are 
                       processed
            returns result, messages
        
        Example: If `Process(images=['highres'],profiles=None)` all versions with
        `source=highres` are updated.

        Events: 
        updateImage(profile)

        """
        if not PILloaded:
            return False, [_(u"Python image library (PIL) not installed.")]
        convert = []
        if not images:
            for p in self.configuration.imageProfiles:
                if not self._CheckCondition(p):
                    continue
                convert.append(p)
        else:
            for p in self.configuration.imageProfiles:
                if not self._CheckCondition(p):
                    continue
                if p.source in images:
                    convert.append(p)
        if not convert:
            return True
        msgs = []
        result = True
        for profile in convert:
            r, m = self._Convert(profile)
            msgs += m
            if not r:
                result = False
            else:
                self.Signal("updateImage", profile=profile)
        return result, msgs
        
        
    def _CheckCondition(self, profile):
        if not hasattr(profile, "condition"):
            return True
        c = ResolveName(profile.condition)
        return c(self)
      
        
    def _Convert(self, profile):
        source = self.files.get(profile.source)
        if not source or not source.tempfile:
            # convert only if tempfile
            return False, ()
        if not source:
            return False, [_(u"Image not found: ") + profile.source]
        p = DvPath()
        p.SetUniqueTempFileName()
        p.SetExtension(profile.extension)
        destPath = str(p)
        
        try:
            source.file.seek(0)
        except:
            pass
        try:
            iObj = Image.open(source)
        except IOError:
            # no file to be converted
            return False, ()
        iObj = iObj.convert("RGB")
        
        # resize
        size = [profile.width, profile.height]
        if size[0] != 0 or size[1] != 0:
            if size[0] == 0:    
                size[0] = size[1]
            elif size[1] == 0:    
                size[1] = size[0]
            x, y = iObj.size
            if x > size[0]: y = y * size[0] / x; x = size[0]
            if y > size[1]: x = x * size[1] / y; y = size[1]
            size = x, y
        
        iObj = iObj.resize(size, Image.ANTIALIAS)
        iObj.save(destPath, profile.format)
        try:
            source.file.seek(0)
        except:
            pass
        
        # file meta data
        imgFile = open(destPath)
        filename = DvPath(profile.dest+"_"+source.filename)
        filename.SetExtension(profile.extension)
        file = File(filekey=profile.dest, 
                    filename=str(filename), 
                    file=imgFile,
                    size=p.GetSize(), 
                    path=destPath, 
                    extension=profile.extension,  
                    tempfile=True)
        self.files.set(profile.dest, file)
        return True, []
        

    def Init(self):
        if PILloaded:
            self.ListenEvent("commit", "ProcessImages")

    def ProcessImages(self):
        images = []
        keys = self.files.keys()
        for p in self.configuration.imageProfiles:
            if p.source in images:
                continue
            if not p.source in keys:
                continue
            f = self.files.get(p.source)
            if not f or not f.tempfile:
                continue
            images.append(p.source)
        self.Process(images=images)


    # from DvPath!!!
    def SetUniqueTempFileName(self):
        """
        () return string
        """
        if not WIN32:
            aDir = tempfile.gettempdir()
            if not aDir:
                return False
            self._path = aDir
            self.AppendSeperator()
            aName = "tmp_" + str(time.time())
            self.SetNameExtension(aName)
            return True

        self._path, x = win32api.GetTempFileName(win32api.GetTempPath(), "tmp_", 0)
        return True



      