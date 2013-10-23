# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

from nive.definitions import IPage
from nive.workflow import WfProcessConf, WfStateConf, WfTransitionConf
from nive_cms.i18n import _


# change pool_state to publish or revoke
def publish(transition, context, user, values):
    context.meta.set("pool_state", 1)
    
def revoke(transition, context, user, values):
    context.meta.set("pool_state", 0)


wfProcess = WfProcessConf(
    id = "default",
    name = _(u"Simple Publishing Workflow"),
    apply = (IPage,),
    states = (
        WfStateConf(
            id = "start",
            name = _(u"New object"),
            actions = ("delete","duplicate","edit","add","remove")
        ),
        WfStateConf(
            id = "edit",
            name = _(u"Edit"),
            actions = ("delete","duplicate","edit","add","remove")
        ),
        WfStateConf(
            id = "public",
            name = _(u"Public"),
            actions = ("delete","duplicate","edit","add","remove")
        )
    ),
    transitions = (
        WfTransitionConf(
            id = "create",
            name = _(u"Create"),
            fromstate = "start",
            tostate = "edit",
            roles = ("group:editor","group:author"),
            actions = ("create",),
            execute = (revoke,)
        ),
        WfTransitionConf(
            id = "publish",
            name = _(u"Publish"),
            fromstate = "edit",
            tostate = "public",
            roles = ("group:editor","group:reviewer"),
            actions = ("publish",),
            execute = (publish,)
        ),
        WfTransitionConf(
            id = "revoke",
            name = _(u"Revoke"),
            fromstate = "public",
            tostate = "edit",
            roles = ("group:editor","group:reviewer"),
            actions = ("revoke",),
            execute = (revoke,)
        )
    )    
)

