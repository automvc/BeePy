from bee.context import HoneyContext
from bee.exception import SqlBeeException
from bee.osql.logger import Logger
from bee.util import HoneyUtil


class BeeSql:

    def select(self, sql, entityClass, params=None):
    # def select(self, sql: str, entityClass: type, params=None) -> list: 
    
        conn = self.__getConn()  
        if conn is None:
            raise SqlBeeException("DB conn is None!")
        
        rs_list = []
        cursor = conn.cursor()
        try: 
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
    
        except Exception as err:  # TODO 异常处理
            Logger.error(f"Error: {err}")  
        finally: 
            # 清理资源  
            if conn is not None:
                conn.close()
        return rs_list


    """ 执行 UPDATE/INSERT/DELETE 操作 """
    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params=None): 
        conn = self.__getConn()
        if conn is None:
            raise SqlBeeException("DB conn is None!")
        cursor = conn.cursor()  
        try: 
            cursor.execute(sql, params or [])
            conn.commit() 
            return cursor.rowcount  # 返回受影响的行数
        except Exception as e: 
            Logger.error(f"Error in modify: {e}")  
            conn.rollback()
            return 0
        finally: 
            if conn is not None:
                conn.close()
                
    def batch(self, sql, params=None):
        conn = self.__getConn()
        if conn is None:
            raise SqlBeeException("DB conn is None!")
        cursor = conn.cursor()  
        try:
            cursor.executemany(sql, params or [])
            conn.commit() 
            return cursor.rowcount  # 返回受影响的行数
        except Exception as e: 
            Logger.error(f"Error in batch: {e}")
            conn.rollback()
            return 0
        finally: 
            if conn is not None:
                conn.close()            
            
    def __getConn(self):
        return HoneyContext.get_connection()
    
