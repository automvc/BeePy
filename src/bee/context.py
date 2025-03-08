# import sqlite3 
# import pymysql
from bee.config import HoneyConfig, PreConfig
from bee.conn_builder import ConnectionBuilder
from bee.factory import BeeFactory
from bee.osql.const import DatabaseConst, SysConst


class HoneyContext: 
    
    dbName=None

    @staticmethod
    def get_connection():
        
        factory = BeeFactory()
        conn = factory.get_connection()
        if conn:
            if HoneyContext.is_active_conn(conn):
                return conn
        
        honeyConfig = HoneyConfig()
        config = honeyConfig.get_db_config_dict()    
        
        HoneyContext.__setDbName(config)
        conn = ConnectionBuilder.build_connect(config)
        factory.set_connection(conn)
        return conn
    
    @staticmethod
    def __setDbName(config):
        if SysConst.dbName in config:
            dbName = config.get(SysConst.dbName, None)
            if dbName:
                HoneyContext.dbName = dbName
    
    @staticmethod
    def get_placeholder():
        
        honeyConfig=HoneyConfig()
        dbName=honeyConfig.get_dbName()
        
        if dbName is None:
            return None
        elif dbName == DatabaseConst.MYSQL.lower() or dbName == DatabaseConst.PostgreSQL.lower(): 
            return "%s"
        elif dbName == DatabaseConst.SQLite.lower(): 
            return "?"
        elif dbName == DatabaseConst.ORACLE.lower(): 
            # query = "SELECT * FROM users WHERE username = :username AND age = :age"
            return ":"
        else:
            return PreConfig.sql_placeholder
            
            
    @staticmethod
    def is_active_conn(conn):
        
        honeyConfig=HoneyConfig()
        dbName=honeyConfig.get_dbName().lower()
        
        if dbName is None:
            return False
        elif dbName == DatabaseConst.MYSQL.lower():
            try:
                conn.ping(reconnect=True)
                return True
            except Exception:
                return False
        # elif dbName == DatabaseConst.SQLite.lower():  
        #     try:  
        #         # SQLite doesn't have a direct way to ping, but we can execute a simple query to check connectivity  
        #         conn.execute('SELECT 1')  
        #         return True  
        #     except Exception:  
        #         return False  
        elif dbName == DatabaseConst.ORACLE.lower():  
            try:  
                # For Oracle, we can use the `ping` method if using cx_Oracle  
                conn.ping()
                return True  
            except Exception:  
                return False  
        # elif dbName == DatabaseConst.PostgreSQL.lower():  
        #     try:  
        #         # PostgreSQL can be checked with a simple query as well  
        #         conn.execute('SELECT 1')  
        #         return True  
        #     except Exception:  
        #         return False
        ## TODO: support other DB   
            
        return False    
            
