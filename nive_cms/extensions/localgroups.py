# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
LocalGroups extension module
----------------------------
Security extension to handle local group assginments for users.
Can be used for Roots and Objects or any other python class supporting events
and id attribute (number). Uses idhash for root objects.
"""

from nive.definitions import ModuleConf, Conf
from nive.definitions import implements, ILocalGroups
from nive.security import Allow, Authenticated, Deny, Everyone

class CMSLocalGroups(object):
    """
    """
    _owner = u"group:owner"
    _secid = None
    implements(ILocalGroups)

    def Init(self):
        self._localRoles = {}
        self.ListenEvent("create", "AddOwner")
        self.ListenEvent("delete", "RemoveGroups")
        self._secid = self._secid or self.id or self.idhash
        # set view permission based on pool_groups. if pool_groups is empty everyone is allowed.
        permission = "view"
        groups = self.meta.get("pool_groups")
        if groups:
            acl = [(Allow, "group:editor", permission),(Allow, "group:author", permission),(Allow, "group:admin", permission)]
            for g in groups:
                if g in (u"authenticated", u"sys:authenticated"):
                    acl.append((Allow, Authenticated, permission))
                else:
                    acl.append((Allow, g, permission))
            acl.append((Deny, Everyone, permission))
            self.__acl__ = tuple(acl)

    @property
    def securityID(self):
        return self._secid

    def GetLocalGroups(self, username, user=None):
        """
        Group assignments use the user name.
        returns a list of all local user groups, including parent settings
        """
        if self.id <= 0:
            return self._LocalGroups(username)
        g = []
        o = self
        while o:
            g += o._LocalGroups(username)
            o = o.parent
        return g 


    def AllLocalGroups(self):
        """
        returns a list of all local user group settings as list including 
        [username, group, id]. This function does not include parent level
        settings.
        """
        return self.db.GetGroups(self.securityID)


    def AddOwner(self, user, **kw):
        """
        Add the current user as group:owner to local roles
        """
        if not user or not str(user):
            return
        self.AddLocalGroup(str(user), self._owner)
    
        
    def AddLocalGroup(self, username, group):
        """
        Add a local group assignment for username.
        """
        groups = self._LocalGroups(username)
        if group in groups:
            return 
        if username==None:
            return
        self._AddLocalGroupsCache(username, group)
        self.db.AddGroup(self.securityID, userid=username, group=group)

        
    def RemoveLocalGroups(self, username, group=None):
        """
        Remove a local group assignment. If group is None all local groups
        will be removed.
        """
        self._DelLocalGroupsCache(username, group)
        self.db.RemoveGroups(self.securityID, userid=username, group=group)


    def RemoveGroups(self, **kw):
        """
        Remove all group assignments before deleting the object. 
        """
        self.db.RemoveGroups(self.securityID)
        self._localRoles = {}
        

    def _LocalGroups(self, username):
        if username in self._localRoles:
            return list(self._localRoles[username])
        g = [r[1] for r in self.db.GetGroups(self.securityID, userid=username)]
        self._localRoles[username] = tuple(g)
        return g
    
    def _AddLocalGroupsCache(self, username, group):
        if username in self._localRoles:
            if group in self._localRoles[username]:
                return
            l = list(self._localRoles[username])
            l.append(group)
            self._localRoles[username] = tuple(l)
            return 
        self._localRoles[username] = (group,)
    
    def _DelLocalGroupsCache(self, username, group=None):
        if not username in self._localRoles:
            return
        if username in self._localRoles and not group:
            del self._localRoles[username]
            return
        if not group in self._localRoles[username]:
            return
        l = list(self._localRoles[username])
        l.remove(group)
        self._localRoles[username] = tuple(l)



def SetupLocalGroups(app, pyramidConfig):
    # get all roots and add extension
    extension = "nive_cms.extensions.localgroups.CMSLocalGroups"
    def add(confs):
        for c in confs:
            e = c.extensions
            if e and extension in e:
                continue
            if e == None:
                e = []
            if isinstance(e, tuple):
                e = list(e)
            e.append(extension)
            c.unlock()
            c.extensions = tuple(e)
            c.lock()
    
    add(app.GetAllRootConfs())
    add(app.GetAllObjectConfs())
    
    
configuration = ModuleConf(
    id = "localGroups",
    name = u"Local Group assignment for objects and roots",
    context = "nive_cms.extensions.localgroups",
    events = (Conf(event="startRegistration", callback=SetupLocalGroups),),
)
