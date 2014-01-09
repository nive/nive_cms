# -*- coding: utf-8 -*-

import unittest

from nive.definitions import *

from nive_cms.extensions.path import *
from nive.security import User
from nive_cms.tests import db_app

from nive.utils import language_data

from nive_cms.tests import __local



class Path(unittest.TestCase):
    
    def setUp(self):
        self.app = db_app.app_nodb()
    
    def tearDown(self):
        pass
    
    
    def test_1(self):
        p = AlternatePath()
        p.app = self.app
        
        fn = p.EscapeFilename(u"this is a filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename("this is a filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename(u"this is a filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename(u"This Is a Filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename(u"This_Is_a_Filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename(u"This_Is_a_Filename/")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename(u"This_Is_a§+#.~$%&_Filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        fn = p.EscapeFilename(u"This Is a looooooooooooooooooooooooooooooooooooooooooooooong Filename")
        self.assert_(fn ==    u"this_is_a_looooooooooooooooooooooooooooooooooooooo", fn)
        
        fn = p.EscapeFilename(u"This Is a loooooooooooooooooooooooooooooooong Filename")
        self.assert_(fn ==    u"this_is_a_loooooooooooooooooooooooooooooooong", fn)
        
        fn = p.EscapeFilename(u"This Is ä Filename")
        self.assert_(fn ==    u"this_is_a_filename", fn)
        
        
    def test_special_chars(self):
        p = AlternatePath()
        p.app = self.app
        
        for lang in language_data.languages:
            conf = language_data.GetConf(lang)
            if not conf.get("special_chars"):
                continue
            
            fn = p.EscapeFilename(u"test " + conf.get("special_chars"))
            self.assert_(fn.startswith(u"test"), fn)
            
        
        
class tWf(__local.DefaultTestCase):

    def setUp(self):
        self._loadApp()
        user = self.user = User(u"test")
        user.groups.append("group:editor")
        root = self.app.root("editor")
        self.page0 = db_app.create_page(root, user)
        self.page = db_app.create_page(self.page0, user)
    
    def tearDown(self):
        user = User(u"test")
        root = self.app.root()
        root.Delete(self.page0.id, user=user)
    
    def test_automated(self):
        title = self.page.meta.title
        filename = self.page.meta.pool_filename
        self.assert_(title!=filename)
        self.assert_(filename==self.page.EscapeFilename(title), filename)

        page2 = db_app.create_page(self.page0, self.user)
        self.assert_(page2.meta.pool_filename!=filename)
        
        page3 = db_app.create_page(self.page0, self.user)
        self.assert_(page3.meta.pool_filename!=filename)
        self.assert_(page3.meta.pool_filename!=page2.meta.pool_filename)
                
        self.assert_(self.page0[filename].id==self.page.id)
        self.assert_(self.page0[filename+u".html"].id==self.page.id)
        self.assert_(self.page0[page2.meta.pool_filename].id==page2.id)
        self.assert_(self.page0[page3.meta.pool_filename].id==page3.id)
        self.assert_(self.page0[str(self.page.id)].id==self.page.id)

        self.assertRaises(KeyError, self.page0.__getitem__, u"nofilename")
        self.assertRaises(KeyError, self.page0.__getitem__, u"9999999999")
        self.assertRaises(KeyError, self.page0.__getitem__, filename+u".html.html")

        
    def test_disabled(self):
        user = User(u"test")
        self.page.data["customfilename"] = True
        self.page.Commit(user=user)
        self.page.meta["pool_filename"] = u"custom"
        self.page.Commit(user=user)
        self.assert_(self.page.meta.pool_filename==u"custom")
        self.page.meta["title"] = u"new title"
        self.page.Commit(user=user)
        self.assert_(self.page.meta.pool_filename==u"custom")
        
        
