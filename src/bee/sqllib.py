from bee.context import HoneyContext
from bee.exception import SqlBeeException, BeeException
from bee.osql.logger import Logger
from bee.util import HoneyUtil


class BeeSql:

    def select(self, sql, entityClass, params=None):
    # def select(self, sql: str, entityClass: type, params=None) -> list: 
    
        conn = self.__getConn()  
        rs_list = []
        try:
            cursor = conn.cursor()
            ## with conn.cursor() as cursor:  # SQLite不支持with语法
            # 执行 SQL 查询  
            cursor.execute(sql, params or [])
            # 获取列名  
            column_names = [description[0] for description in cursor.description]  
            # 获取所有结果  
            results = cursor.fetchall()  
    
            for row in results: 
                # 将行数据映射到新创建的实体对象
                target_obj = HoneyUtil.transform_result(row, column_names, entityClass)  
                rs_list.append(target_obj) 
    
        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)
        return rs_list


    """ 执行 UPDATE/INSERT/DELETE 操作 """
    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params=None):
        conn = self.__getConn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or [])
            conn.commit() 
            return cursor.rowcount  # 返回受影响的行数
        except Exception as e: 
            Logger.error(f"Error in modify: {e}")  
            conn.rollback()
            return 0
        finally: 
            self.__close(cursor, conn)
                
    def batch(self, sql, params=None):
        conn = self.__getConn()
        try:
            cursor = conn.cursor()
            cursor.executemany(sql, params or [])
            conn.commit() 
            return cursor.rowcount  # 返回受影响的行数
        except Exception as e: 
            Logger.error(f"Error in batch: {e}")
            conn.rollback()
            return 0
        finally: 
            self.__close(cursor, conn)
                
                
    def select_fun(self, sql, params=None):
    
        conn = self.__getConn()  
        rs_list = []
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or [])
            result = cursor.fetchone()  # 返回一个元组，例如 (1,)  
            return result[0]
    
        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)
        return rs_list         
            
    def __getConn(self):
        try:
            conn = HoneyContext.get_connection()
        except Exception as e: 
            raise BeeException(e)
        
        if conn is None:
            raise SqlBeeException("DB conn is None!")
        return conn
    
    def __close(self, cursor, conn):
        if cursor is not None:
            cursor.close()
            
        if conn is not None:
            conn.close()
    
