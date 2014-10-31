# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

from nive.utils.utils import ConvertToNumberList

from nive_cms.i18n import _
from nive.definitions import implements, ISort

from nive.definitions import ViewConf
from nive.definitions import IContainer, IPage, IObject, IRoot


class Sort:
    """
    Container sort functionality
    
    Objects can explicitly be sorted and moved up or down in sequence.
    Sort values are stored in meta.pool_sort.
    """
    implements(ISort)


    def GetSort(self):
        """ default sort field for subobjects """
        return u"pool_sort"

    
    def GetSortElements(self, selection=None):
        """ returns the contents as sorted list """
        if selection=="pages":
            return self.GetPages(public=0)
        if selection=="elements":
            return self.GetPageElements()
        return self.GetObjs()
        

    def GetMaxSort(self):
        """ returns the maximum sort number """
        parameter={u"pool_unitref": self.GetID()}
        operators={u"pool_unitref": u"="}
        fields=[u"-max(pool_sort)"]
        root = self.dataroot
        parameter,operators = root.ObjQueryRestraints(self, parameter, operators)
        r = root.Select(parameter=parameter, fields=fields, operators=operators, sort=u"", max=1)
        if len(r):
            s = r[0][0]
            if s==None:
                s=0
            return s
        return 0


    def UpdateSort(self, objs, user):
        """    update pool_sort values according to list """
        if not objs:
            return False, _(u"List is empty")
        if isinstance(objs, basestring):
            objs = ConvertToNumberList(objs)
        ids = []
        for oi in objs:
            # check if listed objects are objects or ids
            if not IObject.providedBy(oi):
                ids.append(int(oi))
        objs2 = []
        if ids:
            # load remaining objects by id
            objs2 = self.GetObjsBatch(ids)
        pos = 10
        processed = []
        for obj in objs:
            if not IObject.providedBy(obj):
                for o in objs2:
                    if o.id == int(obj):
                        obj = o
                        break
            if not IObject.providedBy(obj):
                continue
            if obj.id in processed:
                continue
            processed.append(obj.id)
            obj.meta.set("pool_sort", pos)
            obj.CommitInternal(user)
            pos += 10
        return True, _(u"OK")
        
        
    def InsertAtPosition(self, id, position, user, selection=None):
        """ position = 'first', 'last' or number """
        if position == u"last":
            return self.MoveEnd(id, user=user)
        elif position == u"first":
            return self.MoveStart(id, user=user)
        return self.InsertAfter(id, position, user, selection=selection)


    def InsertBefore(self, id, position, user, selection=None):
        """ insert id before position element id """
        position=int(position)
        order = []
        objs = self.GetSortElements(selection)
        oid = id if not IObject.providedBy(id) else id.id 
        # if id already included in container, remove it
        delpos = -1
        # make sure id is added even if position does not exist
        added = False
        for current in objs:
            if position == current.id:
                order.append(id)
            order.append(current)
            if current.id == oid:
                delpos = len(order)-1
        if delpos > -1:
            del order[delpos]
        if not added:
            order.insert(0, id)
        ok, msgs = self.UpdateSort(order, user=user)
        return ok, msgs


    def InsertAfter(self, id, position, user, selection=None):
        """ insert id after position element id """
        position=int(position)
        order = []
        objs = self.GetSortElements(selection)
        oid = id if not IObject.providedBy(id) else id.id 
        # if id already included in container, remove it
        delpos = -1
        # make sure id is added even if position does not exist
        added = False
        for current in objs:
            order.append(current)
            if current.id == oid:
                delpos = len(order)-1
            if position == current.id:
                order.append(id)
        if delpos > -1:
            del order[delpos]
        if not added:
            order.append(id)
        ok, msgs = self.UpdateSort(order, user=user)
        return ok, msgs


    def MoveUp(self, id, user, selection=None):
        """ move one position up in container """
        objs = self.GetSortElements(selection)
        order = []
        oid = id if not IObject.providedBy(id) else id.id 
        pos = 0
        for obj in objs:
            if obj.id == oid:
                if len(order)==0:
                    return True, []
                order.insert(len(order)-1, obj)
            else:
                order.append(obj)
            
        ok, msgs = self.UpdateSort(order, user=user)
        return ok, msgs


    def MoveDown(self, id, user, selection=None):
        """ move one position down in container """
        objs = self.GetSortElements(selection)
        order = []
        oid = id if not IObject.providedBy(id) else id.id 
        insertID = None
        for obj in objs:
            if obj.id == oid:
                insertID = obj
            else:
                order.append(obj)
                if insertID:
                    order.append(insertID)
                    insertID = None
        if insertID:
            order.append(insertID)
        ok, msgs = self.UpdateSort(order, user=user)
        return ok, msgs
    
    
    def MoveStart(self, id, user, selection=None):
        """ move to top in container """
        objs = self.GetSortElements(selection)
        oid = id if not IObject.providedBy(id) else id.id 
        order = [id]
        for obj in objs:
            if oid == obj.id:
                order[1:].insert(0, obj)
            else:
                order.append(obj)
        ok, msgs = self.UpdateSort(order, user=user)
        return ok, msgs
    
    
    def MoveEnd(self, id, user, selection=None):
        """ move to bottom in container """
        objs = self.GetSortElements(selection)
        oid = id if not IObject.providedBy(id) else id.id 
        lastObj = None
        order = []
        for obj in objs:
            if oid == obj.id:
                lastObj = obj
            else:
                order.append(obj)
        if lastObj:
            order.append(lastObj)
        else:
            order.append(id)
        ok, msgs = self.UpdateSort(order, user=user)
        return ok, msgs


views = [
    # sort
    ViewConf(name = "@sortpages", attr = "sortpages", context = IPage, renderer = "nive_cms.cmsview:sort.pt", permission="edit"),
    ViewConf(name = "@sortpages", attr = "sortpages", context = IRoot, renderer = "nive_cms.cmsview:sort.pt", permission="edit"),
    ViewConf(name="@sortelements",attr="sortelements",context = IContainer, renderer = "nive_cms.cmsview:sort.pt", permission="edit"),
    ViewConf(name = "@moveup",    attr = "moveup",    context = IContainer, permission="edit"),
    ViewConf(name = "@movedown",  attr = "movedown",  context = IContainer, permission="edit"),
    ViewConf(name = "@movetop",   attr = "movetop",   context = IContainer, permission="edit"),
    ViewConf(name = "@movebottom",attr = "movebottom",context = IContainer, permission="edit"),
]    


class SortView:
    """
    View functions for sorting objects
    """

    def sortpages(self):
        """
        display the sortview and editor
        """
        self.ResetFlashMessages()
        result = {u"msgs": [], u"content":"", u"cmsview": self, u"result": False, u"sortelements":[]}
        ids = self.GetFormValue(u"ids")
        sort = self.GetFormValue(u"sort")
        if sort != u"1":
            result[u"sortelements"] = self.context.GetSortElements("pages")
            return result
        ids = ConvertToNumberList(ids)
        if not ids:
            result[u"sortelements"] = self.context.GetSortElements("pages")
            result[u"msgs"] = [_(u"Nothing to sort.")]
            return result
        user = self.User()
        ok, msgs = self.context.UpdateSort(ids, user=user)
        result[u"msgs"] = [msgs]
        result[u"result"] = ok
        result[u"sortelements"] = self.context.GetSortElements("pages")
        return result


    def sortelements(self):
        """
        display the sortview and editor
        """
        self.ResetFlashMessages()
        result = {u"msgs": [], u"content":u"", u"cmsview": self, u"result": False, u"sortelements":[]}
        ids = self.GetFormValue(u"ids")
        sort = self.GetFormValue(u"sort")
        if sort != u"1":
            result[u"sortelements"] = self.context.GetSortElements("elements")
            return result
        ids = ConvertToNumberList(ids)
        if not ids:
            result[u"sortelements"] = self.context.GetSortElements("elements")
            result[u"msgs"] = [_(u"Nothing to sort.")]
            return result
        user = self.User()
        ok, msgs = self.context.UpdateSort(ids, user=user)
        result[u"msgs"] = [msgs]
        result[u"result"] = ok
        result[u"sortelements"] = self.context.GetSortElements("elements")
        return result


    def moveup(self):
        """
        move pageelement one position up in container
        redirect to request.url
        parameter: id, url in request
        """
        self.ResetFlashMessages()
        try:
            id = int(self.GetFormValue(u"id"))
        except:
            id = 0
        if not id:
            ok = False
            msgs = _(u"Not found")
        else:
            ok, msgs = self.context.MoveUp(id, user=self.User())#, selection="elements")
        url = self.GetFormValue(u"url")
        if not url:
            url = self.PageUrl(self.context)
        return self.Redirect(url, [msgs], refresh=ok)


    def movedown(self):
        """
        move pageelement one position down in container
        redirect to request.url
        parameter: id, url in request
        """
        self.ResetFlashMessages()
        try:
            id = int(self.GetFormValue(u"id"))
        except:
            id = 0
        if not id:
            ok = False
            msgs = _(u"Not found")
        else:
            ok, msgs = self.context.MoveDown(id, user=self.User())#, selection="elements")
        url = self.GetFormValue(u"url")
        if not url:
            url = self.PageUrl(self.context)
        return self.Redirect(url, [msgs], refresh=ok)

    
    def movetop(self):
        """
        move pageelement to top in container
        redirect to request.url
        parameter: id, url in request
        """
        self.ResetFlashMessages()
        try:
            id = int(self.GetFormValue(u"id"))
        except:
            id = 0
        if not id:
            ok = False
            msgs = _(u"Not found")
        else:
            ok, msgs = self.context.MoveStart(id, user=self.User())#, selection="elements")
        url = self.GetFormValue(u"url")
        if not url:
            url = self.PageUrl(self.context)
        return self.Redirect(url, [msgs], refresh=ok)
    
    
    def movebottom(self):
        """
        move pageelement to bottom in container
        redirect to request.url
        parameter: id, url in request
        """
        self.ResetFlashMessages()
        try:
            id = int(self.GetFormValue(u"id"))
        except:
            id = 0
        if not id:
            ok = False
            msgs = _(u"Not found")
        else:
            ok, msgs = self.context.MoveEnd(id, user=self.User())#, selection="elements")
        url = self.GetFormValue(u"url")
        if not url:
            url = self.PageUrl(self.context)
        return self.Redirect(url, [msgs], refresh=ok)



    