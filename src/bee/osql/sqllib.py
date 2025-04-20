from bee.context import HoneyContext
from bee.exception import SqlBeeException, BeeException
from bee.osql.logger import Logger

from bee.osql.base import AbstractBase
from bee.osql.cache import CacheUtil
from bee.osql.transform import ParamUtil, ResultUtil


class BeeSql(AbstractBase):

    def select(self, sql, entityClass, params = None):
    # def select(self, sql: str, entityClass: type, params=None) -> list:
    
        cacheObj = CacheUtil.get(sql)
        if cacheObj is not None:
            super().loginfo("---------------get from cache")
            super().loginfo(" | <--  select rows: " + str(len(cacheObj)))
            return cacheObj
        
        conn = self.__getConn()  
        rs_list = []
        try:
            cursor = conn.cursor()
            # # with conn.cursor() as cursor:  # SQLite不支持with语法
            params = ParamUtil.transform_param(params)
            # 执行 SQL 查询  
            cursor.execute(sql, params or [])
            # 获取列名  
            column_names = [description[0] for description in cursor.description]  
            # 获取所有结果  
            results = cursor.fetchall()  
    
            for row in results: 
                # 将行数据映射到新创建的实体对象
                target_obj = ResultUtil.transform_result(row, column_names, entityClass)  
                rs_list.append(target_obj) 
            super().loginfo(" | <--  select rows: " + str(len(rs_list)))
            super().addInCache(sql, rs_list, len(rs_list))
        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)
        return rs_list

    """ 执行 UPDATE/INSERT/DELETE 操作 """

    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params = None):
        conn = self.__getConn()
        a = 0
        try:
            cursor = conn.cursor()
            params = ParamUtil.transform_param(params)
            cursor.execute(sql, params or [])
            conn.commit() 
            a = cursor.rowcount  # 返回受影响的行数
            super().loginfo(" | <--  Affected rows: " + str(a))
            
            if a > 0:
                CacheUtil.clear(sql)
            return a
        except Exception as e: 
            Logger.error(f"Error in modify: {e}")  
            conn.rollback()
            return 0
        finally: 
            self.__close(cursor, conn)
                
    def batch(self, sql, params = None):
        conn = self.__getConn()
        a = 0
        try:
            cursor = conn.cursor()
            params = ParamUtil.transform_list_tuple_param(params)
            cursor.executemany(sql, params or [])
            conn.commit() 
            a = cursor.rowcount  # 返回受影响的行数
            super().loginfo(" | <--  Affected rows: " + str(a))
            
            if a > 0:
                CacheUtil.clear(sql)
                
            return a
        except Exception as e: 
            Logger.error(f"Error in batch: {e}")
            conn.rollback()
            return 0
        finally: 
            self.__close(cursor, conn)
                
    def select_fun(self, sql, params = None):
    
        cacheObj = CacheUtil.get(sql)
        if cacheObj is not None:
            super().loginfo("---------------get from cache")
            super().loginfo(" | <--  select rows: 1")
            return cacheObj
    
        conn = self.__getConn()  
        rs_fun = ''
        try:
            cursor = conn.cursor()
            params = ParamUtil.transform_param(params)
            cursor.execute(sql, params or [])
            result = cursor.fetchone()  # 返回一个元组，例如 (1,)
            if result[0]:
                super().loginfo(" | <--  select rows: 1")
                
                super().addInCache(sql, result[0], 1)
            
            return result[0]
    
        except Exception as e:
            raise SqlBeeException(e)
        finally:
            self.__close(cursor, conn)
            
        return rs_fun        
            
    def __getConn(self):
        try:
            conn = HoneyContext.get_connection()
        except Exception as e: 
            raise BeeException(e)
        
        if not conn:
            raise SqlBeeException("DB conn is None!")
        return conn
    
    def __close(self, cursor, conn):
        if cursor is not None:
            cursor.close()
            
        if conn is not None:
            conn.close()
    
