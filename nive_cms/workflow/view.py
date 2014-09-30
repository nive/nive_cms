# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

from nive_cms.i18n import _
from nive.definitions import IPage
from nive.definitions import IToolboxWidgetConf, IEditorWidgetConf
from nive.definitions import ViewModuleConf, ViewConf, WidgetConf
from nive_cms.cmsview.view import Editor


configuration = ViewModuleConf("nive_cms.cmsview.view.configuration",
    id = "wfview",
    name = _(u"CMS workflow extension"),
    static = "nive_cms.workflow:static",
    permission = "read",
    context = IPage,
    containment = "nive_cms.cmsview.cmsroot.cmsroot",
    view = "nive_cms.workflow.view.WorkflowEdit"
)

configuration.views = [
    ViewConf(name = "@wfWidget", attr = "widget",   renderer = "nive_cms.workflow:templates/widget.pt"),
    ViewConf(name = "@workflow", attr = "workflow", renderer = "nive_cms.workflow:templates/editorpage.pt"),
    ViewConf(name = "@action",   attr = "action"),
    ViewConf(name = "@pubr",     attr = "publishRecursive", permission = "edit")
]

configuration.widgets = [
    WidgetConf(name=_("Workflow"), widgetType=IToolboxWidgetConf, apply=(IPage,), viewmapper="@wfWidget", id="cms.wf",    sort=250),
    WidgetConf(name=_("Workflow"), widgetType=IEditorWidgetConf,  apply=(IPage,), viewmapper="@workflow", id="editor.wf", sort=250)
]


class WorkflowEdit(Editor):

    def widget(self):
        wf = self.context.GetWfInfo(self.User())
        return {u"wf": wf}   
    
    def workflow(self):
        wf = self.context.GetWfInfo(self.User())
        return {u"wf": wf,u"content": u"", u"result": True, u"cmsview":self, u"head": u""}

    def action(self):
        transition = self.GetFormValue(u"t")
        url = self.GetFormValue("redirect_url")
        if not url:
            url = self.PageUrl()
            
        user = self.User()
        self.context.WfAction("", user, transition=transition)
        self.context.CommitInternal(user)
        msg = _(u"OK")
        self.Redirect(url, messages=[msg])
        
    def publishRecursive(self):
        msgs = []
        ok = 0
        user = self.User()
        
        def recursive(self, page, ok):
            for p in page.GetPages(includeMenu=1):
                if not p.meta.pool_state:
                    try:
                        p.WfAction("publish", user)
                        p.CommitInternal(user)
                        msgs.append("Published: " + p.meta.title)
                        ok += 1
                    except Exception, e:
                        msgs.append(u"Failure: "+str(e))
                        pass
                ok = recursive(self, p, ok)
            return ok
        
        ok = recursive(self, self.context, ok)
             
        url = self.GetFormValue("redirect_url")
        if not url:
            url = self.PageUrl()
        msgs.insert(0, "%d pages published!"%ok)
        self.Redirect(url, messages=msgs)
        
