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
            sql,params = self.objToSQL.toSelectSQL(entity)  
            # Logger.log_sql("select SQL: ", sql)  
            Logger.logsql("sql: ", sql)
            Logger.logsql("params: ",params)
            return self.beeSql.select(sql, self.to_class_t(entity),params)  # 返回值用到泛型  
        finally:  
            pass  # 在 Python 中可以省略 finally, 如果没有清理操作  
        
        
    def select_paging(self, entity, start, size): 
        if entity is None: 
            return None  

        try: 
            sql, params = self.objToSQL.toSelectSQLWithPaging(entity,start, size)  
            # Logger.log_sql("select SQL: ", sql)  
            Logger.logsql("sql: ", sql)
            Logger.logsql("params: ",params)
            return self.beeSql.select(sql, self.to_class_t(entity), params)  # 返回值用到泛型  
        finally: 
            pass  
    
    def update(self, entity): 
        if entity is None: 
            return None
        
        try: 
            sql, params = self.objToSQL.toUpdateSQL(entity)  
            Logger.logsql("sql: ", sql)
            Logger.logsql("params: ",params)
            return self.beeSql.modify(sql, params)
        finally: 
            pass  
    
    def insert(self, entity): 
        if entity is None: 
            return None
        
        try: 
            sql, params = self.objToSQL.toInsertSQL(entity)  
            Logger.logsql("sql: ", sql)
            Logger.logsql("params: ",params)
            return self.beeSql.modify(sql, params)
        finally: 
            pass 
        
    def delete(self, entity): 
        if entity is None: 
            return None
        
        try: 
            sql, params = self.objToSQL.toDeleteSQL(entity)  
            Logger.logsql("sql: ", sql)
            Logger.logsql("params: ",params)
            return self.beeSql.modify(sql, params)  
        finally: 
            pass

    def to_class_t(self, entity):
        return type(entity)  #返回实体的类型  
    
    # def __init__(self, beeSql=None, objToSQL=None): 
    #     self._beeSql = beeSql  
    #     self._objToSQL = objToSQL  

    @property  
    def beeSql(self):  
        if self._beeSql is None:  
            # self._beeSql = BeeFactory.get_honey_factory().get_beeSql()  
            self._beeSql =BeeSql()
        return self._beeSql  

    @beeSql.setter  
    def beeSql(self, beeSql):  
        self._beeSql = beeSql  

    @property  
    def objToSQL(self):  
        if self._objToSQL is None:  
            self._objToSQL= ObjToSQL()
        return self._objToSQL  

    @objToSQL.setter  
    def objToSQL(self, objToSQL):  
        self._objToSQL = objToSQL  
        

class SuidRich(Suid):
    
    def insert_batch(self, entity_list): 
        if entity_list is None: 
            return None
        if len(entity_list) == 0:
            return 0
        
        try: 
            sql,list_params = self.objToSQL.toInsertBatchSQL(entity_list)            
            Logger.logsql("sql: ", sql)
            Logger.logsql("params: ", list_params)
            return self.beeSql.batch(sql, list_params)
        finally: 
            pass 
        
