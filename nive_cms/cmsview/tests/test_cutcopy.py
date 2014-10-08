

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

        
class tdbCutCopy(__local.DefaultTestCase):
    
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
        # object functions
        self.text1.CanCopy()
        self.text1.CanPaste()
        
        # container
        self.page.CanCopy()
        self.page.CanPaste()

        root = self.app.root("editor")
        user = User(u"test")
        self.page.Paste([self.text1.id, self.text2.id], 0, user)
        new_texts = self.page.GetObjs()
        self.assert_(len(new_texts)==2)
        
        root.Move([text.id for text in new_texts], 0, user)
        ooo = self.page.GetObjs()
        #self.assertFalse(len(self.page.GetObjs()))
        self.assert_(root.Delete(new_texts[0].id, user))
        self.assert_(root.Delete(new_texts[1].id, user))
        


class tViewCutCopy(__local.DefaultTestCase):

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

        cp = view.SetCopyInfo("copy", [self.text1.id, self.text2.id], self.page)
        self.assert_(cp == ",".join(["copy", str(self.text1.id), str(self.text2.id)]))
        c1, c2 = view.GetCopyInfo()
        self.assert_(c1=="copy")
        self.assert_(len(c2)==2)
        self.assertFalse(view.ClipboardEmpty())
        view.DeleteCopyInfo()
        self.assert_(view.ClipboardEmpty())
        c1, c2 = view.GetCopyInfo()
        self.assert_(c1=="")
        self.assert_(len(c2)==0)

        self.request.GET = {"ids": [self.text1.id, self.text2.id]}
        self.assertRaises(HTTPFound, view.copy)
        c1, c2 = view.GetCopyInfo()
        self.assert_(c1=="copy")
        self.assert_(len(c2)==2)
        view.DeleteCopyInfo()

        self.assertRaises(HTTPFound, view.cut)
        c1, c2 = view.GetCopyInfo()
        self.assert_(c1=="cut")
        self.assert_(len(c2)==2)

        self.assertRaises(HTTPFound, view.copy)
        view.context = self.page
        self.assertRaises(HTTPFound, view.paste)
        new_texts = self.page.GetObjs()
        self.assert_(len(new_texts)==2)
        
        self.request.GET = {"ids": [text.id for text in new_texts]}
        view.context = self.page
        self.assertRaises(HTTPFound, view.cut)
        view.context = self.root
        self.assertRaises(HTTPFound, view.paste)
        ooo = self.page.GetObjs()
        self.assertFalse(len(self.page.GetObjs()))
        self.assert_(self.root.Delete(new_texts[0].id, user))
        self.assert_(self.root.Delete(new_texts[1].id, user))
        


