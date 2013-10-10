import binascii
import os
import getpass
import uuid
import base64

from pyramid.compat import native_

from pyramid.scaffolds import PyramidTemplate # API
from pyramid.scaffolds.template import Template

class DefaultSqliteTemplate(PyramidTemplate):
    _template_dir = 'defaultWebsite'
    summary = 'A simple Nive cms website with Sqlite database'

    def pre(self, command, output_dir, vars):
        """ Overrides :meth:`pyramid.scaffold.template.Template.pre`, adding
        several variables to the default variables list (including
        ``random_string``, and ``package_logger``).  It also prevents common
        misnamings (such as naming a package "site" or naming a package
        logger "root".
        """
        # configuration
        user = None
        while not user:
            user = raw_input("Admin username: ")
        vars['adminuser'] = user
    
        pprompt = lambda: (getpass.getpass('Password: '), getpass.getpass('Retype password: '))
    
        p1, p2 = pprompt()
        while p1 != p2:
            print('Passwords do not match. Try again')
            p1, p2 = pprompt()
        
        vars['adminpass'] = base64.standard_b64encode(p1)

        mail = raw_input("Admin email: ")
        vars['adminemail'] = str(mail)
        
        vars['root'] = raw_input("Root directory for files (default data): ")
        if not vars['root']:
            vars['root'] = "data"

        vars['comment'] = "# SQLite"
        vars['param_website'] = """context="Sqlite3", dbName="%(root)s/website.db" """ % vars
        vars['param_user'] = """context="Sqlite3", dbName="%(root)s/userdb.db" """ % vars
        vars['dbPackage'] = ''
        
        vars['language'] = raw_input("Locale name. Please choose english-> en or german-> de: ")
        
        vars['authsecret'] = str(uuid.uuid4())
        vars['cookiesecret'] = str(uuid.uuid4())

        return PyramidTemplate.pre(self, command, output_dir, vars)
    
    
class DefaultMysqlTemplate(PyramidTemplate):
    _template_dir = 'defaultWebsite'
    summary = 'A simple Nive cms website with Sqlite database'

    def pre(self, command, output_dir, vars):
        """ Overrides :meth:`pyramid.scaffold.template.Template.pre`, adding
        several variables to the default variables list (including
        ``random_string``, and ``package_logger``).  It also prevents common
        misnamings (such as naming a package "site" or naming a package
        logger "root".
        """
        # configuration
        user = None
        while not user:
            user = raw_input("Admin username: ")
        vars['adminuser'] = user
        
        pprompt = lambda: (getpass.getpass('Password: '), getpass.getpass('Retype password: '))
    
        p1, p2 = pprompt()
        while p1 != p2:
            print('Passwords do not match. Try again')
            p1, p2 = pprompt()
            
        vars['adminpass'] = base64.standard_b64encode(p1)
        
        mail = raw_input("Admin email: ")
        vars['adminemail'] = str(mail)

        print "Please enter MySql database settings for the website. Two databases will be used, one for website contents ",
        print "and one to store userdata. Host, port, user and password are used for both databases."
        print ""
        print "The cms will create all required database tables and columns automatically when starting the webserver."
        print "These manual administrator actions are required after running this installation script:"
        print "- Create the two databases"
        print "- Assign create and alter table rights to the database user"
        
        vars['root'] = raw_input("Root directory for files (default data): ")
        if not vars['root']:
            vars['root'] = "data"
            
        vars['dbcontentname'] = raw_input("Content database name (default %s): " % vars["project"])
        if not vars['dbcontentname']:
            vars['dbcontentname'] = vars["project"]
        vars['dbusername'] = raw_input("User database name (default %s_user): "% vars["project"])
        if not vars['dbusername']:
            vars['dbusername'] = vars["project"]+"_user"
        vars['dbhost'] = raw_input("MySql database host (default localhost): ")
        vars['dbport'] = raw_input("MySql database port (leave empty to use default): ")
        vars['dbuser'] = raw_input("MySql database user: ")
            
        pprompt = lambda: (getpass.getpass('Password: '), getpass.getpass('Retype password: '))
    
        p1, p2 = pprompt()
        while p1 != p2:
            print('Passwords do not match. Try again')
            p1, p2 = pprompt()

        vars['dbpass'] = base64.standard_b64encode(p1)
        
        vars['language'] = raw_input("Locale name. Please choose english-> en or german-> de: ")

        vars['comment'] = "# MySql "
        vars['param_website'] = """context="MySql",
            dbName="%(dbcontentname)s",
            host="%(dbhost)s",
            port="%(dbport)s",
            user="%(dbuser)s",
            password=base64.decodestring("%(dbpass)s") """ % vars

        vars['param_user'] = """context="MySql",
            dbName="%(dbusername)s",
            host="%(dbhost)s",
            port="%(dbport)s",
            user="%(dbuser)s",
            password=base64.decodestring("%(dbpass)s") """ % vars
        vars['dbPackage'] = "'MySQL-python'"

        vars['authsecret'] = str(uuid.uuid4())
        vars['cookiesecret'] = str(uuid.uuid4())

        return PyramidTemplate.pre(self, command, output_dir, vars)
