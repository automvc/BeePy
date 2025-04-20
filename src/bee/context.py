# import sqlite3 
# import pymysql
import threading

from bee.config import HoneyConfig
from bee.conn_builder import ConnectionBuilder
from bee.factory import BeeFactory
from bee.osql.const import DatabaseConst, SysConst

from bee.osql.bee_enum import LocalType


class HoneyContext: 
    
    dbname = None

    @staticmethod
    def get_connection():
        
        factory = BeeFactory()
        conn = factory.get_connection()
        if conn:
            if HoneyContext.is_active_conn(conn):
                return conn
        
        config = HoneyConfig().get_db_config_dict()    
        HoneyContext.__setDbName(config)
        conn = ConnectionBuilder.build_connect(config)
        factory.set_connection(conn)
        return conn
    
    @staticmethod
    def __setDbName(config):
        if SysConst.dbname in config:
            dbname = config.get(SysConst.dbname, None)
            if dbname:
                HoneyContext.dbname = dbname
    
    @staticmethod
    def get_placeholder():
        
        dbName = HoneyConfig().get_dbname()
        
        if not dbName:
            return None
        elif dbName == DatabaseConst.MYSQL.lower() or dbName == DatabaseConst.PostgreSQL.lower(): 
            return "%s"
        elif dbName == DatabaseConst.SQLite.lower(): 
            return "?"
        elif dbName == DatabaseConst.ORACLE.lower(): 
            # query = "SELECT * FROM users WHERE username = :username AND age = :age"
            return ":"
        else:
            return HoneyConfig.sql_placeholder
        
    @staticmethod
    def is_active_conn(conn):
        
        dbName = HoneyConfig().get_dbname().lower()
        
        if dbName is None:
            return False
        elif dbName == DatabaseConst.MYSQL.lower():
            try:
                conn.ping(reconnect = True)
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
        # # todo: support other DB   
            
        return False
    
    # 使用单个通用的 thread-local 存储  
    __local_data = threading.local()  

    @staticmethod  
    def _get_storage(): 
        """获取线程存储字典，如果不存在则初始化（静态方法）"""  
        if not hasattr(HoneyContext.__local_data, 'storage'): 
            HoneyContext.__local_data.storage = {}  
        return HoneyContext.__local_data.storage  

    @staticmethod  
    def _set_data(local_type:LocalType, key = None, value = None): 
        """  
        设置线程局部数据（静态方法）  
        :param local_type: DataType 枚举值，指定要存储的数据类型  
        :param key: 存储的key
        :param value: 要存储的值  
        """  
        storage = HoneyContext._get_storage()  
        
        if not value or not key or not key.strip(): 
            return  
        if local_type not in storage: 
            storage[local_type] = {}  
            
        # print("----local------: "+key)
        # print(str(value))
        storage[local_type][key] = value  

    @staticmethod  
    def get_data(local_type:LocalType, key = None): 
        """  
        获取线程局部数据（静态方法）  
        :param local_type: DataType 枚举值  
        :param key: 存储的key
        :return: 存储的值或 None  
        """  
        storage = HoneyContext._get_storage()  
        
        if local_type not in storage or not key: 
            return None  
        return storage[local_type].get(key)  

    @staticmethod  
    def _remove_data(local_type:LocalType, key = None): 
        """  
        移除线程局部数据（静态方法）  
        :param local_type: DataType 枚举值  
        :param key: 存储的key
        """  
        storage = HoneyContext._get_storage()  
        
        if local_type in storage and key: 
            storage[local_type].pop(key, None) 
            
    @staticmethod  
    def _remove_one_local_type(local_type:LocalType): 
        storage = HoneyContext._get_storage()  
        if local_type in storage: 
            storage.pop(local_type, None)  
    
    # __local = threading.local()  
    # @staticmethod
    # def getCacheInfo(sql:str):
    #     if not sql or not hasattr(HoneyContext.__local, '_cache'):  
    #         return None  
    #     return HoneyContext.__local._cache.get(sql) 
    #
    # @staticmethod
    # def _setCacheInfo(sql:str, value:CacheSuidStruct):
    #     if not sql or not sql.strip(): 
    #         return
    #
    #     if not hasattr(HoneyContext.__local, '_cache'): 
    #         HoneyContext.__local._cache = {}  
    #
    #     HoneyContext.__local._cache[sql] = value  
    #
    # @staticmethod
    # def _deleteCacheInfo(sql:str):
    #     pass
    
    @staticmethod
    def isMySql(): 
        dbName = HoneyConfig().get_dbname()
        return dbName == DatabaseConst.MYSQL.lower() 
    
    @staticmethod
    def isSQLite(): 
        dbName = HoneyConfig().get_dbname()
        return dbName == DatabaseConst.SQLite.lower() 
    
    @staticmethod
    def isOracle(): 
        dbName = HoneyConfig().get_dbname()
        return dbName == DatabaseConst.ORACLE.lower() 
    
    @staticmethod
    def get_dbname(): 
        return HoneyConfig().get_dbname()
            
