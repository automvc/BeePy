from bee import SqlUtil
from bee.exception import BeeException, ParamBeeException
from bee.obj2sql import ObjToSQL
from bee.osql.enum import FunctionType, SuidType
from bee.osql.logger import Logger
from bee.sqllib import BeeSql

from bee.base import AbstractCommOperate


class Suid(AbstractCommOperate):
    
    def __init__(self):
        super().__init__()
        self._beeSql = None  
        self._objToSQL = None   
    
    def select(self, entity): 
        if entity is None: 
            return None  

        try: 
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params = self.objToSQL.toSelectSQL(entity)  
            Logger.logsql("select SQL:", sql)
            super().log_params(params)
            list_r= self.beeSql.select(sql, self.to_class_t(entity), params)  # 返回值用到泛型
            return list_r
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturn(list_r)
        
    def update(self, entity): 
        if entity is None: 
            return None
        
        try:
            super().doBeforePasreEntity(entity, SuidType.UPDATE) 
            sql, params = self.objToSQL.toUpdateSQL(entity)  
            Logger.logsql("update SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e) 
        finally:
            super().doBeforeReturnSimple()
    
    def insert(self, entity): 
        if entity is None: 
            return None
        
        try: 
            super().doBeforePasreEntity(entity, SuidType.INSERT)
            sql, params = self.objToSQL.toInsertSQL(entity)  
            Logger.logsql("insert SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()
        
    def delete(self, entity): 
        if entity is None: 
            return None
        
        try: 
            super().doBeforePasreEntity(entity, SuidType.DELETE)
            sql, params = self.objToSQL.toDeleteSQL(entity)  
            Logger.logsql("delete SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()

    def to_class_t(self, entity):
        return type(entity)  # 返回实体的类型  
    
    # def __init__(self, beeSql=None, objToSQL=None): 
    #     self._beeSql = beeSql  
    #     self._objToSQL = objToSQL  

    @property  
    def beeSql(self): 
        if self._beeSql is None: 
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
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params = self.objToSQL.toSelectSQLWithPaging(entity, start, size)  
            Logger.logsql("select_paging SQL:", sql)
            super().log_params(params)
            list_r= self.beeSql.select(sql, self.to_class_t(entity), params)
            return list_r
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturn(list_r)
    
    def insert_batch(self, entity_list): 
        if entity_list is None: 
            return None
        if len(entity_list) == 0:
            return 0
        
        try: 
            super().doBeforePasreListEntity(entity_list)
            sql, list_params = self.objToSQL.toInsertBatchSQL(entity_list)            
            Logger.logsql("insert batch SQL:", sql)
            super().log_params(list_params)
            return self.beeSql.batch(sql, list_params)
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturn()

    def select_first(self, entity):
        # listT = self.select_paging(entity, 0, 2)
        listT = self.select_paging(entity, 0, 1)
        if listT:  # 判断列表是否非空  
            return listT[0]  # 返回首个元素  
        return None 
    
    def select_by_id(self, entity_class, *ids):
        # self.check_for_by_id(entity_class, ids)
        
        if not entity_class:
            raise ParamBeeException("entity_class can not be empty!")
        
        if not ids:
            raise ParamBeeException("id can not be None when call select_by_id!") 
        
        try:
            id_list = list(ids)
            super().doBeforePasreEntity(entity_class, SuidType.SELECT)
            sql = self.objToSQL.toSelectByIdSQL(entity_class, len(id_list))
            Logger.logsql("select by id SQL:", sql)
            super().log_params(id_list)
            return self.beeSql.select(sql, entity_class, id_list) 
        except Exception as e: 
            raise BeeException(e)
        finally:
            # super().doBeforeReturn()         
            super().doBeforeReturnSimple()         
    
    def delete_by_id(self, entity_class, *ids):
        if not entity_class:
            raise ParamBeeException("entity_class can not be empty!")
        
        if not ids:
            raise ParamBeeException("id can not be None when call select_by_id!") 
        
        try: 
            id_list = list(ids)
            super().doBeforePasreEntity(entity_class, SuidType.DELETE)
            sql = self.objToSQL.toDeleteById(entity_class, len(id_list))
            Logger.logsql("delete by id SQL:", sql)
            super().log_params(id_list)
            return self.beeSql.modify(sql, id_list)  
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()

    def select_fun(self, entity, functionType, field_for_fun):
        if entity is None:
            return None  

        try: 
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params = self.objToSQL.toSelectFunSQL(entity, functionType, field_for_fun)
            Logger.logsql("select fun SQL:", sql)
            super().log_params(params)
            r = self.beeSql.select_fun(sql, params)
            if  r is None and functionType == FunctionType.COUNT:
                return 0
            else:
                return r
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()
    
    def count(self, entity):
        return self.select_fun(entity, FunctionType.COUNT, "*")

    def exist(self, entity):
        r = self.count(entity)
        return r > 0 
    
    def create_table(self, entityClass, is_drop_exist_table=None):
        if is_drop_exist_table:
            sql0 = self.objToSQL.toDropTableSQL(entityClass)
            Logger.logsql("drop table SQL:", sql0)
            self.beeSql.modify(sql0)
        sql = self.objToSQL.toCreateSQL(entityClass)
        Logger.logsql("create table SQL:", sql)
        return self.beeSql.modify(sql)
    
    def index_normal(self, entity_class, fields, index_name=None): 
        prefix = "idx_"  
        index_type_tip = "normal"  
        index_type = ""  # normal will be empty  
        self._index(entity_class, fields, index_name, prefix, index_type_tip, index_type)  

    def unique(self, entity_class, fields, index_name=None): 
        prefix = "uie_"  
        index_type_tip = "unique"  
        index_type = "UNIQUE "
        self._index(entity_class, fields, index_name, prefix, index_type_tip, index_type)  

    def _index(self, entity_class, fields, index_name, prefix, index_type_tip, index_type): 
        index_sql = self.objToSQL.to_index_sql(entity_class, fields, index_name, prefix, index_type_tip, index_type)  
        self._index_modify(index_sql)  

    def _index_modify(self, index_sql): 
        Logger.logsql("create index SQL:", index_sql)  
        self.beeSql.modify(index_sql)
    
    def drop_index(self, entity_class, index_name=None):
        sql = self.objToSQL.to_drop_index_sql(entity_class, index_name)
        Logger.logsql("drop index SQL:", sql)
        self.beeSql.modify(sql)


# for custom SQL
class PreparedSql(AbstractCommOperate):
    
    """
    eg:
    """ 
    def select(self, sql, return_type_class, params=None, start=None, size=None):
        if sql is None: 
            return None  
        if return_type_class is None: 
            return None  
        try:
            sql = SqlUtil.add_paging(sql, start, size)
            
            Logger.logsql("select SQL(PreparedSql):", sql)
            super().log_params(params)
            return self.beeSql.select(sql, return_type_class, params)  # 返回值用到泛型  
        except Exception as e: 
            raise BeeException(e)
        
       
        
    """
    eg:
      preparedSql=PreparedSql()
      entity_list =preparedSql.select_dict("SELECT * FROM orders WHERE name=#{name} and id=#{id} and name=#{name}", Orders, params_dict ={"name":"bee1","id":4})
    """ 
    def select_dict(self, sql, return_type_class, params_dict=None, start=None, size=None):
        if params_dict:
            sql, params_dict = SqlUtil.transform_sql(sql, params_dict)  
        return self.select(sql, return_type_class, params_dict, start, size)
    
    """
    eg:
        sql = "update orders set name = ?, remark = ? where id = ?"
        params = ('bee130', 'test-update', 1)
        updateNum = preparedSql.modify(sql, params)
    """     
    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params=None): 
        try: 
            Logger.logsql("modify SQL(PreparedSql):", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)
    
    """
    eg:
        sql = "update orders set name = #{name}, remark = #{remark} where id = #{id}"
        params_dict={"id":1, "name":"newName","remark":"remark2"}
        updateNum = preparedSql.modify_dict(sql, params_dict)
    """        

    def modify_dict(self, sql, params_dict=None):
        if params_dict: 
            sql, params_dict = SqlUtil.transform_sql(sql, params_dict)
        return self.modify(sql, params_dict)
    
    
    def __init__(self): 
        super().__init__()
        self._beeSql = None  
        self._objToSQL = None   
        
    @property
    def beeSql(self): 
        if self._beeSql is None: 
            self._beeSql = BeeSql()
        return self._beeSql  

    @beeSql.setter  
    def beeSql(self, beeSql): 
        self._beeSql = beeSql 
        
