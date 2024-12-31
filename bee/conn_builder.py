# import sqlite3 
# import pymysql
import importlib

from bee.key import Key
from bee.osql.const import DatabaseConst
from bee.osql.logger import Logger

class ConnectionBuilder:
    
    @staticmethod
    def build_connect(config):
        dbName = None
        if Key.dbName in config:
            tempConfig = config.copy()
            dbName = tempConfig.pop(Key.dbName, None)
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
        
        if Key.dbModuleName in config:   #优先使用dbModuleName，让用户可以有选择覆盖默认配置的机会
            dbModuleName = tempConfig.pop(Key.dbModuleName, None)
        elif dbName not in db_modules:
            # raise ValueError(f"Database type '{dbName}' is not supported, need config dbModuleName.")      
            print(f"Database type '{dbName}' is not supported, need config dbModuleName.")
            return None
        else:
            dbModuleName = db_modules[dbName]
        
            
        db_module = importlib.import_module(dbModuleName)  
        Logger.info(f"Use  {dbModuleName}!")
        
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
# def fetch_user_data_postgresql(username, age):
#     connection = psycopg2.connect(
#         host='localhost',
#         user='your_username',
#         password='your_password',
#         database='your_database'
#     )




# import cx_Oracle
#
# def fetch_user_data_oracle(username, age):
#     connection = cx_Oracle.connect('username/password@localhost/orcl')

# Or
# import cx_Oracle  
#
# # 创建数据库连接  
# def create_connection():  
#     dsn = cx_Oracle.makedsn("hostname", 1521, service_name="your_service_name")  
#     connection = cx_Oracle.connect(user="your_username", password="your_password", dsn=dsn)  
#     return connection  
