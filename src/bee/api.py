from bee import SqlUtil
from bee.exception import BeeException
from bee.obj2sql import ObjToSQL
from bee.osql.logger import Logger
from bee.sqllib import BeeSql


class Suid:
    
    def __init__(self): 
        self._beeSql = None  
        self._objToSQL = None   
    
    def select(self, entity): 
        if entity is None: 
            return None  

        try: 
            # a=1/0
            sql, params = self.objToSQL.toSelectSQL(entity)  
            Logger.logsql("select SQL:", sql)
            Logger.logsql("params:", params)
            return self.beeSql.select(sql, self.to_class_t(entity), params)  # 返回值用到泛型  
        except Exception as e: 
            raise BeeException(e)
            # raise BeeException("aaaaa")
        
    def update(self, entity): 
        if entity is None: 
            return None
        
        try: 
            sql, params = self.objToSQL.toUpdateSQL(entity)  
            Logger.logsql("update SQL:", sql)
            Logger.logsql("params:", params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e) 
    
    def insert(self, entity): 
        if entity is None: 
            return None
        
        try: 
            sql, params = self.objToSQL.toInsertSQL(entity)  
            Logger.logsql("insert SQL:", sql)
            Logger.logsql("params:", params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e)
        
    def delete(self, entity): 
        if entity is None: 
            return None
        
        try: 
            sql, params = self.objToSQL.toDeleteSQL(entity)  
            Logger.logsql("delete SQL:", sql)
            Logger.logsql("params:", params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)

    def to_class_t(self, entity):
        return type(entity)  # 返回实体的类型  
    
    # def __init__(self, beeSql=None, objToSQL=None): 
    #     self._beeSql = beeSql  
    #     self._objToSQL = objToSQL  

    @property  
    def beeSql(self): 
        if self._beeSql is None: 
            # self._beeSql = BeeFactory.get_honey_factory().get_beeSql()  
            self._beeSql = BeeSql()
        return self._beeSql  

    @beeSql.setter  
    def beeSql(self, beeSql): 
        self._beeSql = beeSql  

    @property  
    def objToSQL(self): 
        if self._objToSQL is None: 
            self._objToSQL = ObjToSQL()
        return self._objToSQL  

    @objToSQL.setter  
    def objToSQL(self, objToSQL): 
        self._objToSQL = objToSQL  
        

class SuidRich(Suid):
    
    def select_paging(self, entity, start, size): 
        if entity is None: 
            return None  

        try: 
            sql, params = self.objToSQL.toSelectSQLWithPaging(entity, start, size)  
            Logger.logsql("select_paging SQL:", sql)
            Logger.logsql("params:", params)
            return self.beeSql.select(sql, self.to_class_t(entity), params)  # 返回值用到泛型  
        finally: 
            pass      
    
    def insert_batch(self, entity_list): 
        if entity_list is None: 
            return None
        if len(entity_list) == 0:
            return 0
        
        try: 
            sql, list_params = self.objToSQL.toInsertBatchSQL(entity_list)            
            Logger.logsql("insert batch SQL:", sql)
            Logger.logsql("params:", list_params)
            return self.beeSql.batch(sql, list_params)
        finally: 
            pass 

    def select_first(self, entity):
        listT = self.select_paging(entity, 0, 2)
        if listT:  # 判断列表是否非空  
            return listT[0]  # 返回首个元素  
        return None 

# for custom SQL
class PreparedSql:
    
    """
    eg:
    """ 
    def select(self, sql, return_type, params=None, start=None, size=None):  # TODO 参数类型？？？
        if sql is None: 
            return None  
        if return_type is None: 
            return None  
        try:
            sql = SqlUtil.add_paging(sql, start, size)
            # print(".............."+sql)
            
            Logger.logsql("select SQL(PreparedSql):", sql)
            Logger.logsql("params:", params)
            return self.beeSql.select(sql, return_type, params)  # 返回值用到泛型  
        except Exception as e: 
            raise BeeException(e)
        
       
        
    """
    eg: select * from orders where userid=#{userid}
    """ 

    def select_dict(self, sql, return_type, params_dict=None, start=None, size=None):
        transformed_sql, params = SqlUtil.transform_sql(sql, params_dict)  
        return self.select(transformed_sql, return_type, params, start, size)
    
    """
    eg:
    """     
    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params=None): 
        try: 
            Logger.logsql("modify SQL(PreparedSql):", sql)
            Logger.logsql("params:", params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)
    
    """
    eg:
    """        
    def modify_dict(self, sql, dict_params=None): 
        pass
    
    
    def __init__(self): 
        self._beeSql = None  
        self._objToSQL = None   
        
    @property
    def beeSql(self): 
        if self._beeSql is None: 
            # self._beeSql = BeeFactory.get_honey_factory().get_beeSql()  
            self._beeSql = BeeSql()
        return self._beeSql  

    @beeSql.setter  
    def beeSql(self, beeSql): 
        self._beeSql = beeSql 
        
