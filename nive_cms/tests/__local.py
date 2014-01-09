

import sys
from nive.definitions import DatabaseConf


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

