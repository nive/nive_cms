# -*- coding: utf-8 -*-

import time
import unittest

from pyramid import testing 
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render

from nive_cms.tests.db_app import *

from nive_cms.cmsview.view import *
from nive_cms.workflow.view import WorkflowEdit
from nive_cms.workflow import wf

from nive_cms.tests.__local import DB_CONF


class tWf(unittest.TestCase):

    def _loadApp(self, mods=None):
        if not mods:
            mods = []
        mods.append(DatabaseConf(DB_CONF))
        self.app = app(mods)

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        request.content_type = ""
        self.config = testing.setUp(request=request)
        self.request = request
        self._loadApp(["nive_cms.workflow.wf.wfProcess", "nive_cms.workflow.view"])
        self.app.Startup(self.config)
        self.root = self.app.root()
        user = User(u"test")
        user.groups.append("group:editor")
        self.page = create_page(self.root, user)
        self.request.context = self.page

    def tearDown(self):
        user = User(u"test")
        testing.tearDown()
        root = self.app.root()
        self.root.Delete(self.page.id, user=user)
        self.app.Close()


    def test_functions(self):
        user = User(u"test")
        user.groups.append("group:editor")
        wf.publish(None, self.page, user, {})
        self.assert_(self.page.meta.pool_state==1)
        wf.revoke(None, self.page, user, {})
        self.assert_(self.page.meta.pool_state==0)

    
    def test_views1(self):
        view = WorkflowEdit(self.page, self.request)
        self.assertRaises(HTTPFound, view.action)
        self.assertRaises(HTTPFound, view.publishRecursive)
        view.widget()
        view.workflow()
        
    
    def test_templates(self):
        user = User(u"test")
        user.groups.append("group:editor")
        view = WorkflowEdit(self.page, self.request)
        vrender = {"context":self.page, "view":view, "request": self.request, "cmsview":view}
        values = view.widget()
        values.update(vrender)
        render("nive_cms.workflow:templates/widget.pt", values)
        values = view.workflow()
        values.update(vrender)
        render("nive_cms.workflow:templates/editorpage.pt", values)

        
