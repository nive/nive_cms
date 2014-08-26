
## Welcome to Nive cms
Nive is professional out the box content management system for mobile and desktop websites based on 
python and the webframework pyramid. 
Please refer to the website cms.nive.co for detailed information.

## Version
The package will soon be released as stable 1.0 version. For a better package management the previous
`nive` package has been split up into several smaller packages.

If you are updating from version 0.9.11 or older please read `nive/update-0.9.11-to-1.0.txt`.
If you are updating from version 0.9.12 read `changes.txt`.

## Source code
The source code is hosted on github: https://github.com/nive/nive_cms

## Documentation and installation
http://cms.nive.co

### Translations
Translations can be extracted using lingua>=3.2

    > pip install lingua-3.2
    > bin/pot-create -o nive_cms/locale/nive_cms.pot nive_cms
    
### Third party modules 
Some included modules have their own license:

- bootstrap (nive_cms.design.static.bootstrap)
- jquery / jquery-ui / jquery.form
- iconset (nive_cms.cmsview.static.images) by Mark James http://www.famfamfam.com/ 

