# import sqlite3
# import pymysql
import importlib

from bee.osql.const import DatabaseConst, SysConst
from bee.osql.logger import Logger


class ConnectionBuilder:
    '''
    Connection Builder.
    '''

    _already_print = False

    @staticmethod
    def build_connect(config):
        '''
        build connect via dict config
        :param config:
        '''
        dbname = None
        if SysConst.dbname in config:
            tempConfig = config.copy()
            dbname = tempConfig.pop(SysConst.dbname, None)
        else:
            tempConfig = config

        # Map database names to their respective module names and connection functions
        db_modules = {
            DatabaseConst.MYSQL.lower(): 'pymysql',
            DatabaseConst.SQLite.lower(): 'sqlite3',
            DatabaseConst.ORACLE.lower(): 'cx_Oracle',
            DatabaseConst.PostgreSQL.lower(): 'psycopg2',
        }

        # Check if the dbname is supported
        # if dbname not in db_modules:

        if dbname is None:
            # raise ValueError("Need set the dbname in Config!")
            Logger.info("Need set the dbname in Config!")
            return None

        original_dbname = dbname
        dbname = dbname.lower()

        if SysConst.dbModuleName in config:  # 优先使用dbModuleName，让用户可以有选择覆盖默认配置的机会
            dbModuleName = tempConfig.pop(SysConst.dbModuleName, None)
        elif dbname not in db_modules:
            # raise ValueError(f"Database type '{dbname}' is not supported, need config dbModuleName.")
            # todo
            Logger.warn(f"Database type '{dbname}' is not supported, need config dbModuleName.")
            return None
        else:
            dbModuleName = db_modules[dbname]

        db_module = importlib.import_module(dbModuleName)
        if not ConnectionBuilder._already_print:
            Logger.info(f"Database driver use {dbModuleName} for {original_dbname}")
            ConnectionBuilder._already_print = True

        conn = None
        # Now create the connection using the imported module
        if dbname == DatabaseConst.MYSQL.lower():
            conn = db_module.connect(**tempConfig)
        elif dbname == DatabaseConst.SQLite.lower():
            conn = db_module.connect(**tempConfig)
        elif dbname == DatabaseConst.ORACLE.lower():
            conn = db_module.connect(**tempConfig)
        elif dbname == DatabaseConst.PostgreSQL.lower():
            conn = db_module.connect(**tempConfig)
        else:
            Logger.warn(f"Do support database type: {dbname}")

        return conn

# ### 2. 使用 `psycopg2`（PostgreSQL）
#
# ```python
# import psycopg2
#
#     connection = psycopg2.connect(
#         host='localhost',
#         user='your_username',
#         password='your_password',
#         database='your_database'
#     )

# import cx_Oracle
#
# connection = cx_Oracle.connect('username/password@localhost/orcl')

# Or
# import cx_Oracle
#
# # 创建数据库连接
#     dsn = cx_Oracle.makedsn("hostname", 1521, service_name="your_service_name")
#     connection = cx_Oracle.connect(user="your_username", password="your_password", dsn=dsn)
#     return connection
