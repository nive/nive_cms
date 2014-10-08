

import unittest

from pyramid import testing
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render


from nive_cms.cmsview.view import Editor
from nive.security import User
from nive.definitions import DatabaseConf
from nive_cms.cmsview.sort import *

from nive_cms.tests import db_app
from nive_cms.tests import __local
        
class tdbSort(__local.DefaultTestCase):
    
    def setUp(self):
        self._loadApp()
        root = self.app.root("editor")
        user = User(u"test")
        user.groups.append("group:editor")
        self.page = db_app.create_page(root, user)
        self.text1 = db_app.create_text(root, user)
        self.text2 = db_app.create_text(root, user)
        pass
    
    def tearDown(self):
        root = self.app.root()
        user = User(u"test")
        user.groups.append("group:editor")
        try:
            root.Delete(self.page.id, user=user)
        except:
            pass
        try:
            root.Delete(self.text1.id, user=user)
        except:
            pass
        try:
            root.Delete(self.text2.id, user=user)
        except:
            pass
    

    def test_functions(self):
        root = self.app.root("editor")
        user = User(u"test")
        request = {"pepos": 0}
        
        self.assert_(root.GetSort())
        
        self.assert_(root.GetSortElements(selection=None))
        self.assert_(root.GetSortElements(selection="pages"))
        self.assert_(root.GetSortElements(selection="elements"))

        self.assert_(root.GetMaxSort())
        root.UpdateSort([self.text2, self.text1], user)
        
        root.InsertAtPosition(self.text1.id, u"first", user, selection=None)
        root.InsertAtPosition(self.text1.id, u"last", user, selection=None)
        root.InsertAtPosition(self.text1.id, self.text2.id, user, selection=None)

        root.InsertBefore(self.text1.id, self.text2.id, user, selection=None)
        root.InsertAfter(self.text1.id, self.text2.id, user, selection=None)
        
        root.MoveUp(self.text1.id, user, selection=None)
        root.MoveDown(self.text1.id, user, selection=None)
        root.MoveStart(self.text1.id, user, selection=None)
        root.MoveEnd(self.text1.id, user, selection=None)
        
        # element selection
        root.InsertAtPosition(self.text1.id, u"first", user, selection="elements")
        root.InsertAtPosition(self.text1.id, u"last", user, selection="elements")
        root.InsertAtPosition(self.text1.id, self.text2.id, user, selection="elements")

        root.InsertBefore(self.text1.id, self.text2.id, user, selection="elements")
        root.InsertAfter(self.text1.id, self.text2.id, user, selection="elements")
        
        root.MoveUp(self.text1.id, user, selection="elements")
        root.MoveDown(self.text1.id, user, selection="elements")
        root.MoveStart(self.text1.id, user, selection="elements")
        root.MoveEnd(self.text1.id, user, selection="elements")



class tViewSort(__local.DefaultTestCase):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        request.content_type = ""
        self.request = request
        self.config = testing.setUp(request=request)
        self.config.include('pyramid_chameleon')
        self._loadApp()
        self.app.Startup(self.config)
        self.root = self.app.root("editor")
        user = User(u"test")
        user.groups.append("group:editor")
        self.page = db_app.create_page(self.root, user)
        self.text1 = db_app.create_text(self.root, user)
        self.text2 = db_app.create_text(self.root, user)
        self.request.context = self.page

    def tearDown(self):
        user = User(u"test")
        self.root.Delete(self.page.id, user=user)
        self.app.Close()
        testing.tearDown()

    def test_views1(self):
        view = Editor(self.page, self.request)
        user = User(u"test")
        user.groups.append("group:editor")

        view.sortpages()
        view.sortelements()
        
        self.request.GET = {"id": self.text1.id}
        self.assertRaises(HTTPFound, view.moveup)
        self.assertRaises(HTTPFound, view.movedown)
        self.assertRaises(HTTPFound, view.movetop)
        self.assertRaises(HTTPFound, view.movebottom)


