# -*- coding: utf-8 -*-

import unittest

from nive.helper import FormatConfTestFailure

from nive_cms import app, box, column, file, image, link, media, menublock, news, note, page, root
from nive_cms import spacer, text, codeblock




class TestConf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_conf1(self):
        r=app.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf3(self):
        r=box.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf4(self):
        r=column.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf5(self):
        r=file.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf7(self):
        r=image.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf8(self):
        r=link.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf9(self):
        r=media.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf10(self):
        r=menublock.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf11(self):
        r=news.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf12(self):
        r=note.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf13(self):
        r=page.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf14(self):
        r=root.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf15(self):
        r=spacer.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf16(self):
        r=text.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf17(self):
        r=codeblock.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

