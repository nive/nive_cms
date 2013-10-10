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
Extensions for easier Page, Column and Page element handling.
"""

import string
from datetime import datetime

from nive.utils.utils import ConvertToList
from nive.definitions import StagPage, StagPageElement
from nive.security import Allow, Deny, Authenticated, Everyone


class PageContainer:
    """
    Extension for page containers. Adds sub page selection functionality.
    """

    def GetPages(self, includeMenu=1, hidden=1, public=None):
        """
        Returns sub pages as objects based on parameters. ::
        
            includeMenu = include pages marked as menus
            hidden = include hidden pages
            public = only published pages (pool_state=1). if none 
                     queryRestraint default is used
            
        returns object list
        """
        parameter, operators = {},{}
        parameter[u"pool_stag"] = (StagPage, StagPageElement-1)
        operators[u"pool_stag"] = u"BETWEEN"
        if public==1:
            parameter[u"pool_state"] = 1
        elif public==0:
            if u"pool_state" in parameter:
                del parameter[u"pool_state"]
        pages = self.GetObjs(parameter = parameter, operators = operators)
        if includeMenu and hidden:
            return pages
        p2 = []
        for p in pages:
            if not includeMenu and p.data["navMenu"]:
                continue
            if not hidden and p.data["navHidden"]:
                continue
            p2.append(p)
        return p2


    def GetPagesList(self, includeMenu=1, hidden=1, public=None, fields=None):
        """
        Returns sub pages as objects based on parameters. ::
        
            includeMenu = include pages marked as menus
            hidden = include hidden pages
            public = only published pages (pool_state=1). if none 
                     queryRestraint default is used
            fields = fields names included in result
            
        returns object list
        """
        if not fields:
            fields = [u"title", u"header", u"description", u"keywords",
                      u"navMenu", u"navHidden",
                      u"pool_state", u"pool_wfa", u"pool_unitref", u"pool_stag", u"pool_filename"]
        parameter, operators = {},{}
        parameter[u"pool_stag"] = (StagPage, StagPage+9)
        operators[u"pool_stag"] = u"BETWEEN"
        parameter[u"pool_unitref"] = self.id
        if public==1:
            parameter[u"pool_state"] = 1
        elif public==0:
            if u"pool_state" in parameter:
                del parameter[u"pool_state"]
        if not hidden:
            parameter[u"navHidden"] = 0
        if not includeMenu:
            parameter[u"navMenu"] = 0
        sort = self.GetSort()
        root = self.dataroot
        parameter,operators = root.ObjQueryRestraints(self, parameter, operators)
        pages = root.SelectDict(pool_type=u"page", parameter=parameter, fields=fields, operators=operators, sort=sort, dontAddType=True)
        return pages


    def GetElementsList(self, fields=None):
        """
        Returns sub pages as objects based on parameters. ::
        
            fields = fields names included in result
            
        returns object list
        """
        if not fields:
            fields = [u"id", u"type", u"pool_filename", u"pool_unitref", u"pool_stag"]
        parameter, operators = {},{}
        parameter[u"pool_stag"] = (StagPageElement, StagPageElement+9)
        operators[u"pool_stag"] = u"BETWEEN"
        parameter[u"pool_unitref"] = self.id
        sort = self.GetSort()
        root = self.dataroot
        parameter,operators = root.ObjQueryRestraints(self, parameter, operators)
        pages = root.SelectDict(pool_type=u"page", parameter=parameter, fields=fields, operators=operators, sort=sort, dontAddType=True)
        return pages


class PageElementContainer:
    """
    Adds page element container functions to the object.
    """

    # Contained page elements/editor -------------------------------------------------------------

    @property
    def page(self):
        return self

    def IsEmpty(self):
        """
        Check for empty page with no elements on it
        
        returns True/False
        """
        return len(self.GetPageElements()) == 0


    def GetPageElements(self, addBoxContents=0, addColumnContents=0, **kw):
        """
        List all contained elements. ::
        
            addBoxContents = add elements contained in boxes
            skipColumns = do not include columns
            kw = passed to GetObj() internally
            
        returns a list of elements
        """
        # b.w. 0.9.9
        if kw.get("skipColumns")!=None:
            addColumnContents = not bool(kw.get("skipColumns"))
        parameter, operators = {},{}
        parameter[u"pool_stag"] = StagPageElement
        if not addColumnContents:
            parameter[u"pool_type"] = u"column"
            operators[u"pool_type"] = u"!="
        elements = self.GetObjs(parameter = parameter, operators = operators, **kw)
        if not addBoxContents and not addColumnContents:
            return elements
        elements2 = []
        for e in elements:
            t = e.GetTypeID()
            if addBoxContents and t == "box":
                elements2 += e.GetPageElements(addBoxContents, addColumnContents, **kw)
            elif addColumnContents and t == "column":
                elements2 += e.GetPageElements(addBoxContents, addColumnContents, **kw)
        return elements + elements2


    def AllowedPageElements(self, user, group=None):
        """
        Return a list of page element configurations allowed to be added in
        this container
        """
        elements = []
        for t in self.app.GetAllObjectConfs():
            if t["selectTag"] == StagPageElement and not t.get("hidden"):
                elements.append(t)
        return elements


    def GetElementContainer(self):
        """ return the current element container """
        return self

    def GetPage(self):
        """ return the current page """
        return self



class PageElement:
    """
    Adds page element functionality to objects.
    
    Sets local acl 's based on object.meta.pool_group settings.
    """
    
    @property
    def page(self):
        return self.parent.page

    def Init(self):
        self.ListenEvent("commit", self.TouchPage)
        groups = self.meta.get("pool_groups")
        if groups:
            groups = ConvertToList(groups)
            acl = [(Allow, "group:editor", "view"),(Allow, "group:author", "view"),(Allow, "group:admin", "view")]
            for g in groups:
                if g == u"authenticated":
                    acl.append((Allow, Authenticated, "view"))
                else:
                    acl.append((Allow, g, "view"))
            acl.append((Deny, Everyone, 'view'))
            self.__acl__ = acl 


    def GetElementContainer(self):
        """ Returns the current element container """
        return self.parent


    def GetPage(self):
        """ Return the current page """
        return self.parent.GetPage()
    
    
    def TouchPage(self, user=None):
        """ Changes the change date and time of the containing page to now """
        try:
            # calls touch for the page
            self.page.CommitInternal(user=user) 
        except AttributeError:
            self.page.meta[u"pool_change"]=datetime.now()
    

class PageColumns:
    """
    Column support for pages.
    
    Columns are always referenced by *name* and only one column for each name 
    is created locally. *Local* means columns may be loaded from parent pages
    if not existing in this object.
    
    Checks whether a column already exists before it is created.
    """
    
    def Init(self):
        self.ListenEvent("beforeAdd", "_CheckColumn")

    
    def GetColumn(self, name):
        """
        Returns the column *name* as object. If no local column is found, parents 
        searched.  
        """
        c = self.LocalColumn(name)
        if c:
            return c
        parent = self.parent
        while parent:
            c = parent.LocalColumn(name)
            if c:
                return c
            if parent.GetID() == 0:
                break
            parent = parent.parent
        return None
        

    def GetProxiedColumn(self, name):
        """
        Returns the column *name* as object. If no local column is found, parents 
        searched.  
        """
        c = self.LocalColumn(name)
        if c:
            return c
        parent = self.parent
        while parent:
            c = parent.LocalColumn(name)
            if c:
                c.__parent__ = self
                return c
            if parent.GetID() == 0:
                break
            parent = parent.parent
        return None
        

    def HasLocalColumn(self, name):
        """
        Returns if a local column *name* exists. 
        """
        parameter = {u"pool_type": u"column", u"title": name}
        operators = {u"pool_type": u"=", u"title": u"="}
        columns = self.GetObjsList(fields = [u"id"], parameter=parameter, operators=operators)
        if not len(columns):
            return False
        return True

        
    def LocalColumn(self, name):
        """
        Returns the local column *name* as object or None.
        """
        parameter = {u"pool_type": u"column", u"title": name}
        operators = {u"pool_type": u"=", u"title": u"="}
        columns = self.GetObjs(parameter=parameter, operators=operators)
        if not len(columns):
            return None
        return columns[0]
        
    
    def _CheckColumn(self, data, type, **kw):    
        """
        Checks if new column is going to be created and if already one exists
        """
        if type != u"column":
            return
        name = data.get("title")
        c = self.LocalColumn(name)
        if not c:
            return
        raise TypeError, "Column exists (%s)" % (name)
    
