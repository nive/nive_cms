# -*- coding: utf-8 -*-

import unittest

from nive.workflow import WorkflowNotAllowed
from nive.security import Allow, Deny, Authenticated, Everyone, User

from nive_cms.tests.db_app import *
from nive_cms.tests import __local


class ObjectTest_db(object):
    """
    Actual test classes are subclassed for db system (sqlite, mysql)
    """

    def setUp(self):
        self._loadApp()
        self.remove = []
        
    def tearDown(self):
        u = User(u"test")
        u.groups.append("group:editor")
        root = self.app.root("editor")
        for r in self.remove:
            root.Delete(r, u)
    
    def test_root(self):
        a=self.app
        ccc = a.db.GetCountEntries()
        r=root(a)
        user = User(u"test")
        user.groups.append("group:editor")
        # add to root
        p = create_page(r, user=user)
        self.assert_(p)
        self.remove.append(p.id)
        b0 = create_menublock(r, user=user)
        self.assert_(b0)
        self.remove.append(b0.id)
        b1 = create_box(r, user=user)
        self.assert_(b1)
        self.remove.append(b1.id)
        col = r.GetColumn("left")
        if col:
            r.Delete(col.id, user=user)
        b2 = create_column(r, user=user)
        self.assert_(b2)
        self.remove.append(b2.id)
        b3 = create_file(r, user=user)
        self.assert_(b3)
        self.remove.append(b3.id)
        b4 = create_image(r, user=user)
        self.assert_(b4)
        self.remove.append(b4.id)
        b5 = create_media(r, user=user)
        self.assert_(b5)
        self.remove.append(b5.id)
        b6 = create_note(r, user=user)
        self.assert_(b6)
        self.remove.append(b6.id)
        b7 = create_text(r, user=user)
        self.assert_(b7)
        self.remove.append(b7.id)
        b8 = create_spacer(r, user=user)
        self.assert_(b8)
        self.remove.append(b8.id)
        b9 = create_link(r, user=user)
        self.assert_(b9)
        self.remove.append(b9.id)
        b10 = create_code(r, user=user)
        self.assert_(b10)
        self.remove.append(b10.id)
        r.Delete(p.id, user=user, obj=p)
        r.Delete(b0.id, user=user)
        r.Delete(b1.id, user=user)
        r.Delete(b2.id, user=user)
        r.Delete(b3.id, user=user)
        r.Delete(b4.id, user=user)
        r.Delete(b5.id, user=user)
        r.Delete(b6.id, user=user)
        r.Delete(b7.id, user=user)
        r.Delete(b8.id, user=user)
        r.Delete(b9.id, user=user)
        r.Delete(b10.id, user=user)
        self.assertEqual(ccc, a.db.GetCountEntries(), "Delete failed")
        
        # workflow failure add to root
        user.groups = ["group:looser"]
        self.assertRaises(WorkflowNotAllowed, create_page, r, user)


    def test_page(self):
        a=self.app
        ccc = a.db.GetCountEntries()
        r=root(a)
        user = User(u"test")
        user.groups.append("group:editor")
        # add to root
        p = create_page(r, user=user)
        self.assert_(p)
        self.remove.append(p.id)
        
        self.assert_(p.IsLinked()==u"")
        self.assert_(p.IsPage())
        p.meta["pool_groups"] = ["sys:authenticated","another"]
        p.Signal("init")

        r = p
        b0 = create_menublock(r, user=user)
        self.assert_(b0)
        b1 = create_box(r, user=user)
        self.assert_(b1)
        b2 = create_column(r, user=user)
        self.assert_(b2)
        b3 = create_file(r, user=user)
        self.assert_(b3)
        b4 = create_image(r, user=user)
        self.assert_(b4)
        b5 = create_media(r, user=user)
        self.assert_(b5)
        b6 = create_note(r, user=user)
        self.assert_(b6)
        b7 = create_text(r, user=user)
        self.assert_(b7)
        b8 = create_spacer(r, user=user)
        self.assert_(b8)
        b9 = create_link(r, user=user)
        self.assert_(b9)
        b10 = create_code(r, user=user)
        self.assert_(b10)
        root(a).Delete(r.id, user=user, obj=r)
        self.assertEqual(ccc, a.db.GetCountEntries(), "Delete failed")
        
    def test_container(self):
        a=self.app
        ccc = a.db.GetCountEntries()
        r=root(a)
        user = User(u"test")
        user.groups.append("group:editor")
        # add to root
        b1 = create_box(r, user=user)
        self.assert_(b1)
        self.remove.append(b1.id)
        r = b1
        b3 = create_file(r, user=user)
        self.assert_(b3)
        b4 = create_image(r, user=user)
        self.assert_(b4)
        b5 = create_media(r, user=user)
        self.assert_(b5)
        b6 = create_note(r, user=user)
        self.assert_(b6)
        b7 = create_text(r, user=user)
        self.assert_(b7)
        b8 = create_spacer(r, user=user)
        self.assert_(b8)
        b9 = create_link(r, user=user)
        self.assert_(b9)
        b0 = create_menublock(r, user=user)
        self.assert_(b0)
        b10 = create_code(r, user=user)
        self.assert_(b10)
        
        r=root(a)
        col = r.GetColumn("left")
        if col:
            r.Delete(col.id, user=user)
        b2 = create_column(r, user=user)
        self.assert_(b2)
        self.remove.append(b2.id)
        r = b2
        b3 = create_file(r, user=user)
        self.assert_(b3)
        b4 = create_image(r, user=user)
        self.assert_(b4)
        b5 = create_media(r, user=user)
        self.assert_(b5)
        b6 = create_note(r, user=user)
        self.assert_(b6)
        b7 = create_text(r, user=user)
        self.assert_(b7)
        b8 = create_spacer(r, user=user)
        self.assert_(b8)
        b9 = create_link(r, user=user)
        self.assert_(b9)
        b0 = create_menublock(r, user=user)
        self.assert_(b0)
        b10 = create_code(r, user=user)
        self.assert_(b10)
        root(a).Delete(b1.id, user=user, obj=b1)
        root(a).Delete(b2.id, user=user, obj=b2)
        self.assertEqual(ccc, a.db.GetCountEntries(), "Delete failed")

    def test_objs(self):
        a=self.app
        ccc = a.db.GetCountEntries()
        r=root(a)
        user = User(u"test")
        user.groups.append("group:editor")
        p = create_page(r, user=user)
        self.remove.append(p.id)
        r = p
        #box
        b1 = create_box(r, user=user)
        b1.IsContainer()
        b1.GetPage()
        b1.GetElementContainer()
        b1.GetContainer()
        #column
        b2 = create_column(r, user=user)
        self.assert_(b2.IsLocal(r))
        b2.GetName()
        b2.IsContainer()
        b2.GetPage()
        b2.GetPages()
        b2.GetElementContainer()
        b2.GetContainer()
        self.assert_(b2.GetColumn("left")==b2)
        #file
        b3 = create_file(r, user=user)
        b3.GetDownloadTitle()
        b3.FilenameToTitle()
        #menublock
        b0 = create_menublock(r, user=user)
        b0.GetMenuPages()
        
        root(a).Delete(r.id, user=user)
        self.assertEqual(ccc, a.db.GetCountEntries(), "Delete failed")
        


class ObjectTest_db_Sqlite(ObjectTest_db, __local.SqliteTestCase):
    """
    see tests.__local
    """
            
class ObjectTest_db_MySql(ObjectTest_db, __local.MySqlTestCase):
    """
    see tests.__local
    """

class ObjectTest_db_pg(ObjectTest_db, __local.PostgreSqlTestCase):
    """
    see tests.__local
    """



