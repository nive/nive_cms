# -*- coding: utf-8 -*-
# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
This file contains all base classes for subclassing your own objects. All required components
are already included as parent classes.
"""

from nive.components.baseobjects import (
        ApplicationBase,
        RootBase,
        RootReadOnlyBase,
        ObjectBase,
        ObjectReadOnlyBase,
        ObjectContainerBase,
        ObjectContainerReadOnlyBase
)
from nive.definitions import implements
from nive.definitions import IPage, IPageContainer, IPageElement, IFile, IPageElementContainer, IFolder
from nive.helper import DecorateViewClassWithViewModuleConf

# page elements for subclassing --------------------------------------------

from nive_cms.extensions.path import AlternatePath, AlternateRootPath
from nive_cms.extensions.pages import PageContainer, PageElementContainer, PageElement, PageColumns
from nive_cms.cmsview.sort import Sort
from nive_cms.cmsview.cutcopy import ObjCopy, ContainerCopy

class PageBase(ContainerCopy, Sort, AlternatePath, PageColumns, PageContainer, PageElementContainer, ObjectContainerBase):
    """
    *Page with content element support*
    
    - stored in database
    - rendered as website page
    - handles sub pages
    - handles page columns
    - is an element container
    - supports paste of elements and pages
    - contained pages and elements are sortable 
    
    Interfaces: ``IPage, IPageContainer, IPageElementContainer, IContainer, IObject``
    """
    implements(IPage, IPageContainer, IPageElementContainer)


class PageRootBase(ContainerCopy, Sort, AlternateRootPath, PageColumns, PageContainer, PageElementContainer, RootBase):
    """
    *Root with content element support*
    
    - handles sub pages
    - handles page columns
    - rendered as website page
    - is an element container
    - supports paste of elements and pages
    - contained pages and elements are sortable 
    
    Interfaces: ``IPageContainer, IPageElementContainer, IContainer, IRoot``
    """
    implements(IPageContainer, IPageElementContainer)


class PageElementBase(ObjCopy, PageElement, ObjectBase):
    """
    *Page element* 
    
    - stored in database
    - does not store subobjects
    - stored in element containers 
    - cut, copy and paste support
    
    Interfaces: ``INonContainer, IObject, IPageElement``
    """
    implements(IPageElement)


class PageElementFileBase(ObjCopy, PageElement, ObjectBase):
    """
    *Page element with file download support*
    
    - stored in database
    - does not store subobjects
    - stored in element containers 
    - cut, copy and paste support
    - contained files can be downloaded

    Interfaces: ``INonContainer, IObject, IPageElement, IFile``
    """
    implements(IPageElement, IFile)


class PageElementContainerBase(Sort, ContainerCopy, PageElementContainer, ObjectContainerBase):
    """
    *Element container*
    
    - stored in database
    - handles page elements
    - supports paste of elements and pages
    - contained pages and elements are sortable 

    Interfaces: ``IContainer, IObject, IPageElement, IPageElementContainer``
    """
    implements(IPageElement, IPageElementContainer)


class FolderBase(ContainerCopy, PageElement, ObjectContainerBase):
    """
    *Resource container*
    
    - stored in database
    - handles files and resource objects
    - supports paste of elements
    """
    implements(IFolder)
    
    

# design view base class --------------------------------------------

from nive.views import BaseView
from nive.helper import ResolveName
from nive.definitions import ICMSRoot, IViewModuleConf, IPage

class DesignBase(BaseView):
    """
    *Website design base class*
    
    - lookup view module automatically
    - load editor instance
    """
    
    def __init__(self, context, request):
        super(DesignBase, self).__init__(context, request)
        # the viewModule is used for template/template directory lookup
        #if not self.viewModule:
        #    raise ConfigurationError, "'design' view module configuration not found"

    def view(self):
        # redirect if page is linked
        if IPage.providedBy(self) and self.context.IsLinked():
            return self.Redirect(self.context.data["pagelink"])
        values = {u"cmsview": self.editorview, u"context": self.context, u"view": self}
        return self.DefaultTemplateRenderer(values)

    @property
    def editorview(self):
        """
        Tries to load the editor view class. If none is registered the function 
        will simply return None. Otherwise the editor view class instance with 
        context and request set.
        """
        if hasattr(self, "_c_editor"):
            return self._c_editor
        # restrict editor to roots with ICMSRoot Interface. Otherwise the editor views
        # will not be found 
        root = self.context.dataroot
        if not ICMSRoot.providedBy(root):
            return None
        module = self.context.app.QueryConfByName(IViewModuleConf, "editor")
        if not module:
            return None
        cls =  DecorateViewClassWithViewModuleConf(module, module.view)
        editor = cls(self.context, self.request)
        self._c_editor = editor
        return editor
            

    def IsEditmode(self):
        try:
            return self.request.editmode
        except:
            return False
        