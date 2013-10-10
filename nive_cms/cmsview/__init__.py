
from nive.definitions import ModuleConf

configuration = ModuleConf(
    id="cms-view-module",
    name="Meta package to load cms editor components",
    modules=(
        "nive_cms.cmsview.cmsroot", 
        "nive_cms.cmsview.view", 
        "nive_cms.cmsview.admin", 
        "nive.components.reform.reformed"
    ),
)