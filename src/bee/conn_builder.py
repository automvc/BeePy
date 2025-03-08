# import sqlite3 
# import pymysql
import importlib

from bee.osql.const import DatabaseConst, SysConst
from bee.osql.logger import Logger


class ConnectionBuilder:
    
    _already_print=False
    
    @staticmethod
    def build_connect(config):
        dbName = None
        if SysConst.dbName in config:
            tempConfig = config.copy()
            dbName = tempConfig.pop(SysConst.dbName, None)
        else:
            tempConfig = config
            
        # Map database names to their respective module names and connection functions  
        db_modules = {
            DatabaseConst.MYSQL.lower(): 'pymysql',
            DatabaseConst.SQLite.lower(): 'sqlite3',  
            DatabaseConst.ORACLE.lower(): 'cx_Oracle',  
            DatabaseConst.PostgreSQL.lower(): 'psycopg2',  
        }  
        
        # Check if the dbName is supported  
        # if dbName not in db_modules:  
        
        if dbName is None:
            # raise ValueError("Need set the dbName in Config!")
            Logger.info("Need set the dbName in Config!")
            return None
        
        dbName = dbName.lower()
        
        if SysConst.dbModuleName in config:   #优先使用dbModuleName，让用户可以有选择覆盖默认配置的机会
            dbModuleName = tempConfig.pop(SysConst.dbModuleName, None)
        elif dbName not in db_modules:
            # raise ValueError(f"Database type '{dbName}' is not supported, need config dbModuleName.")      
            Logger.info(f"Database type '{dbName}' is not supported, need config dbModuleName.") # TODO
            return None
        else:
            dbModuleName = db_modules[dbName]
        
            
        db_module = importlib.import_module(dbModuleName)
        if not ConnectionBuilder._already_print:
            Logger.info(f"Database driver use: {dbModuleName}!")
            ConnectionBuilder._already_print=True
        
        # Now create the connection using the imported module  
        if dbName == DatabaseConst.MYSQL.lower(): 
            return db_module.connect(**tempConfig)  
        elif dbName == DatabaseConst.SQLite.lower(): 
            return db_module.connect(**tempConfig)




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
