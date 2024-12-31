# import sqlite3 
# import pymysql
from bee.config import HoneyConfig
from bee.conn_builder import ConnectionBuilder
from bee.factory import BeeFactory
from bee.key import Key
from bee.osql.const import DatabaseConst


class HoneyContext: 
    
    dbName=None

    @staticmethod 
    def get_connection():
        
        factory = BeeFactory()
        conn = factory.get_connection()
        if conn is not None:
        #     conn.ping(reconnect=True)  #重新获取，要重连。  只是mysql?
            return conn
        
        honeyConfig = HoneyConfig()
        config = honeyConfig.get_db_config_dict()    
        
        HoneyContext.__setDbName(config)
        conn = ConnectionBuilder.build_connect(config)
        factory.set_connection(conn)
        return conn
    
    @staticmethod
    def __setDbName(config):
        if Key.dbName in config:
            dbName = config.get(Key.dbName, None)
            if dbName is not None:
                HoneyContext.dbName = dbName
    
    @staticmethod
    def get_placeholder():
        
        honeyConfig=HoneyConfig()
        dbName=honeyConfig.get_dbName().lower()
        
        if dbName is None:
            return None
        elif dbName == DatabaseConst.MYSQL.lower() or dbName == DatabaseConst.PostgreSQL.lower(): 
            return "%s"
        elif dbName == DatabaseConst.SQLite.lower(): 
            return "?"
        elif dbName == DatabaseConst.ORACLE.lower(): 
            # query = "SELECT * FROM users WHERE username = :username AND age = :age"
            return ":"
            
        
        #还要有set的方法，或在配置文件中设置  TODO
