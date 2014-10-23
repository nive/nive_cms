# -*- coding: utf-8 -*-

import unittest

from nive.utils.path import DvPath
from nive.definitions import AppConf, DatabaseConf
from nive.portal import Portal
from nive_cms.app import WebsitePublisher
from nive import File


def app_db(confs=None):
    appconf = AppConf("nive_cms.app")
    a = WebsitePublisher()
    a.Register(appconf)
    if confs:
        for c in confs:
            a.Register(c)
    p = Portal()
    p.Register(a)
    a.Startup(None)
    dbfile = DvPath(a.dbConfiguration.dbName)
    if not dbfile.IsFile():
        dbfile.CreateDirectories()
    try:
        a.Query("select id from pool_meta where id=1")
        a.Query("select id from box where id=1")
        a.Query("select id from columnbox where id=1")
        a.Query("select id from texts where id=1")
        a.Query("select id from pool_files where id=1")
    except:
        a.GetTool("nive.tools.dbStructureUpdater")()
    return a

def app_nodb():
    appconf = AppConf("nive_cms.app")
    a = WebsitePublisher()
    a.Register(appconf)
    a.Register(DatabaseConf())
    p = Portal()
    p.Register(a)
    #a.Startup(None)
    return a

def emptypool(app):
    db = app.db
    db.Query(u"delete FROM pool_meta")
    db.Query(u"delete FROM pool_files")
    db.Query(u"delete FROM pool_fulltext")
    db.Query(u"delete FROM pool_groups")
    db.Query(u"delete FROM pool_sys")
    import shutil
    shutil.rmtree(str(db.root), ignore_errors=True)
    db.root.CreateDirectories()

def createpool(path,app):
    path.CreateDirectories()
    app.GetTool("nive.tools.dbStructureUpdater")()


def root(a):
    r = a.GetRoot()
    return r

def create_page(c, user):
    type = "page"
    data = {"header": u"the header", "title": u"the title"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_box(c, user):
    type = "box"
    data = {}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_column(c, user):
    type = "column"
    data = {"title":u"left"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_file(c, user):
    type = "file"
    data = {"title":u"download", "file": File(filename=u"file2.txt", file=u"this is a textfile")}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_image(c, user):
    type = "image"
    data = {"title":u"nice", "image": File(filename="blank.gif", file=bytes("\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"))}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_media(c, user):
    type = "media"
    data = {"title":u"nice"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_note(c, user):
    type = "note"
    data = {"title":u"note", "textblock":u"this is a note text"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_text(c, user):
    type = "text"
    data = {"title":u"text", "textblock":u"this is a long text"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_spacer(c, user):
    type = "spacer"
    data = {"cssClass":u"h1"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_link(c, user):
    type = "link"
    data = {"title":u"a link", "linkurl": u"http://www.nive.net"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_menublock(c, user):
    type = "menublock"
    data = {"title":u"nice", "menutype": u"tree"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_code(c, user):
    type = "code"
    data = {"codetype": u"raw", "codeblock": u"<script>alert('hello!');</script>"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o

def create_news(c, user):
    type = "news"
    data = {"title":u"a link", "text": u"a text", "publish": "2012-12-12", "link": u"http://www.nive.net"}
    o = c.Create(type, data = data, user = user)
    #o.Commit()
    return o



