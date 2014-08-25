
## Welcome to Nive cms
Nive is professional out the box content management system for mobile and desktop websites based on 
python and the webframework pyramid. 
Please refer to the website cms.nive.co for detailed information.

## Version
This version is a beta release. The application is stable and complete. The public API as documented 
on the website is stable will not change. 

## Source code
The source code is hosted on github: https://github.com/nive/nive_cms

## Documentation and installation
http://cms.nive.co

### Translations
Translations can be extracted using lingua>=3.1

    > pip install lingua-3.1
    > bin/pot-create -o nive_cms/locale/nive_cms.pot nive_cms
    
### Third party modules 
Some included modules have their own license:

- bootstrap (nive_cms.design.static.bootstrap)
- jquery / jquery-ui / jquery.form
- iconset (nive_cms.cmsview.static.images) by Mark James http://www.famfamfam.com/ 

