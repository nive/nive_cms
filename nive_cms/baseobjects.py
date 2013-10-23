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


# page elements for subclassing --------------------------------------------

from nive_cms.extensions.path import AlternatePath
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


class PageRootBase(ContainerCopy, Sort, AlternatePath, PageColumns, PageContainer, PageElementContainer, RootBase):
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