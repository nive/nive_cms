

import sys
import unittest
from nive.definitions import DatabaseConf
from nive_cms.tests import db_app

# real database test configuration
# change these to fit your system
ENABLE_MYSQL_TESTS = True
try:
    import MySQLdb
except ImportError:
    ENABLE_MYSQL_TESTS = False


WIN = sys.platform == "win32"

# sqlite and mysql
if WIN:
    ROOT = "c:\\Temp\\nive_cms\\"
else:
    ROOT = "/var/tmp/nive_cms/"


DB_CONF = DatabaseConf(
    dbName = ROOT+"cms.db",
    fileRoot = ROOT,
    context = "Sqlite3"
)


MYSQL_CONF = DatabaseConf(
    context = "MySql",
    dbName = "ut_nive_cms",
    host = "localhost",
    user = "root",
    password = "",
    port = "",
    fileRoot = ROOT
)



# essential system tests are run for both database systems if installed.
# These switches also allow to manually enable or disable database system tests.
ENABLE_SQLITE_TESTS = True
ENABLE_MYSQL_TESTS = True
try:
    import MySQLdb
except ImportError:
    ENABLE_MYSQL_TESTS = False


if ENABLE_SQLITE_TESTS:

    class SqliteTestCase(unittest.TestCase):
        def _loadApp(self, mods=None):
            if not mods:
                mods = []
            mods.append(DatabaseConf(DB_CONF))
            self.app = db_app.app_db(mods)

else:

    class SqliteTestCase(object):
        def _loadApp(self, mods=None):
            pass


if ENABLE_MYSQL_TESTS:

    class MySqlTestCase(unittest.TestCase):
        def _loadApp(self, mods=None):
            if not mods:
                mods = []
            mods.append(DatabaseConf(MYSQL_CONF))
            self.app = db_app.app_db(mods)

else:

    class MySqlTestCase(object):
        def _loadApp(self, mods=None):
            pass

# Higher level tests are only run for one database system, not multiple.
# The database type can be switched here
DefaultTestCase = SqliteTestCase
