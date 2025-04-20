from typing import overload

from bee.context import HoneyContext
from bee.exception import BeeException, ParamBeeException
from bee.osql import SqlUtil

from bee.condition import Condition, ConditionImpl
from bee.osql.base import AbstractCommOperate
from bee.osql.bee_enum import FunctionType, SuidType, LocalType
from bee.osql.obj2sql import ObjToSQL
from bee.osql.sqllib import BeeSql
from bee.osql.struct import CacheSuidStruct


class Suid(AbstractCommOperate):
    
    def __init__(self):
        super().__init__()
        self._beeSql = None  
        self._objToSQL = None   
    
    @overload
    def select(self, entity):
        ...
        
    @overload    
    def select(self, entity, condition: Condition):
        ... 
        
    def __select(self, entity): 
        list_r = None
        try: 
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params, table_name = self.objToSQL.toSelectSQL(entity) 
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context(sql, params, table_name, "list<T>", entityClass)
             
            super().logsql("select SQL:", sql)
            super().log_params(params)
            list_r = self.beeSql.select(sql, entityClass, params)
            return list_r
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturn(list_r)
        
    def update(self, entity): 
        if not entity:
            return None
        
        try:
            super().doBeforePasreEntity(entity, SuidType.UPDATE) 
            sql, params, table_name = self.objToSQL.toUpdateSQL(entity)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context2(sql, params, table_name, "int", entityClass, SuidType.UPDATE)
              
            super().logsql("update SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e) 
        finally:
            super().doBeforeReturnSimple()
    
    def insert(self, entity): 
        if not entity: 
            return None
        
        try: 
            super().doBeforePasreEntity(entity, SuidType.INSERT)
            sql, params, table_name = self.objToSQL.toInsertSQL(entity) 
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context2(sql, params, table_name, "int", entityClass, SuidType.INSERT)
             
            super().logsql("insert SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()
            
    @overload
    def delete(self, entity):
        ...
        
    @overload    
    def delete(self, entity, condition: Condition):
        ...
        
    def __delete(self, entity): 
        try: 
            super().doBeforePasreEntity(entity, SuidType.DELETE)
            sql, params, table_name = self.objToSQL.toDeleteSQL(entity)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context2(sql, params, table_name, "int", entityClass, SuidType.DELETE)
              
            super().logsql("delete SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()
    
    # since 1.6.0        
    def select(self, entity, condition: Condition = None): 
        if not entity:
            return None
        
        if not condition:
            return self.__select(entity)
        
        list_r = None
        try: 
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params, table_name = self.objToSQL.toSelectSQL2(entity, condition)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context(sql, params, table_name, "list<T>", entityClass)  
            
            super().logsql("select SQL:", sql)
            super().log_params(params)
            list_r = self.beeSql.select(sql, entityClass, params)
            return list_r
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturn(list_r)
    
    # since 1.6.0        
    def delete(self, entity, condition: Condition = None): 
        if not entity: 
            return None
        
        if not condition:
            return self.__delete(entity)
        
        try: 
            super().doBeforePasreEntity(entity, SuidType.DELETE)
            sql, params, table_name = self.objToSQL.toDeleteSQL2(entity, condition)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context2(sql, params, table_name, "int", entityClass, SuidType.DELETE)
            
            super().logsql("delete SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()

    def _to_class_t(self, entity):
        return type(entity)  # 返回实体的类型 
    
    def _reg_cache_in_context(self, sql, params, table_name, returnType, entityClass):
        
        HoneyContext._set_data(LocalType.CacheSuidStruct, sql, CacheSuidStruct(sql, params, table_name, returnType, entityClass, SuidType.SELECT))
        
    def _reg_cache_in_context2(self, sql, params, table_name, returnType, entityClass, suidType):
        
        HoneyContext._set_data(LocalType.CacheSuidStruct, sql, CacheSuidStruct(sql, params, table_name, returnType, entityClass, suidType)) 
    
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
    
    @overload
    def select_paging(self, entity, start, size): 
        ...
        
    @overload
    def select_paging(self, entity, start, size, *selectFields):
        ...
    
    def select_paging(self, entity, start, size, *selectFields):
        
        if not selectFields:
            return self.__select_paging(entity, start, size)
        
        condition = ConditionImpl()
        condition.selectField(*selectFields)
        condition.start(start).size(size)
        return super().select(entity, condition)
        
    def __select_paging(self, entity, start, size): 
        if not entity: 
            return None  

        try: 
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params, table_name = self.objToSQL.toSelectSQLWithPaging(entity, start, size)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context(sql, params, table_name, "list<T>", entityClass)
              
            super().logsql("select_paging SQL:", sql)
            super().log_params(params)
            list_r = self.beeSql.select(sql, entityClass, params)
            return list_r
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturn(list_r)
    
    def insert_batch(self, entity_list): 
        if not entity_list: 
            return None
        if len(entity_list) == 0:
            return 0
        
        try: 
            super().doBeforePasreListEntity(entity_list, SuidType.INSERT)
            sql, list_params, table_name = self.objToSQL.toInsertBatchSQL(entity_list)   
            
            entityClass = self._to_class_t(entity_list[0])
            self._reg_cache_in_context2(sql, list_params, table_name, "int", entityClass, SuidType.INSERT)
                     
            super().logsql("insert batch SQL:", sql)
            super().log_params_for_batch(list_params)
            return self.beeSql.batch(sql, list_params)
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()

    def select_first(self, entity):
        
        start = 0
        size = 2
        if HoneyContext.isMySql() or HoneyContext.isSQLite():
            size = 1
        elif HoneyContext.isOracle():
            start = 1
        
        listT = self.select_paging(entity, start, size)
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
            sql, table_name = self.objToSQL.toSelectByIdSQL(entity_class, len(id_list))
            
            self._reg_cache_in_context(sql, id_list, table_name, "<T>", entity_class)
            
            super().logsql("select by id SQL:", sql)
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
            sql, table_name = self.objToSQL.toDeleteById(entity_class, len(id_list))
            
            self._reg_cache_in_context2(sql, id_list, table_name, "int", entity_class, SuidType.DELETE)
            
            super().logsql("delete by id SQL:", sql)
            super().log_params(id_list)
            return self.beeSql.modify(sql, id_list)  
        except Exception as e: 
            raise BeeException(e)
        finally:
            super().doBeforeReturnSimple()

    def select_fun(self, entity, functionType, field_for_fun):
        if not entity:
            return None  

        try: 
            super().doBeforePasreEntity(entity, SuidType.SELECT)
            sql, params, table_name = self.objToSQL.toSelectFunSQL(entity, functionType, field_for_fun)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context(sql, params, table_name, "<T>", entityClass)
            
            super().logsql("select fun SQL:", sql)
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
    
    # /**
    # * Update record according to whereFields.
    # * @param entity table's entity(do not allow null).
    # * <br>Fields that are not specified as whereFields, as part of the set(only non empty and non null fields 
    # * <br>are processed by default).
    # * @param condition Condition as filter the record.
    # * @param whereFields As a field list of where part in SQL, multiple fields can separated by commas in one 
    # * <br>whereField parameter or use variable parameter (the fields in the list will be used as where filter)
    # * <br>But if id's value is null can not as filter.
    # * <br>Notice:the method op of condition also maybe converted to the where expression.
    # * @return the numbers of update record(s) successfully,if fails, return integer less than 0.
    # * @since 1.6.0
    # */
    def updateBy(self, entity, condition: Condition = None, *whereFields):
        if not entity: 
            return None
        # the op method in condition can as whereFields
        # if not whereFields or len(whereFields) == 0 or (len(whereFields) == 1 and (not whereFields[0] or whereFields[0].isspace())):
        #     raise ParamBeeException("whereFields at least include one field.")
        
        try:
            super().doBeforePasreEntity(entity, SuidType.UPDATE) 
            sql, params, table_name = self.objToSQL.toUpdateBySQL2(entity, condition, whereFields)
            
            entityClass = self._to_class_t(entity)
            self._reg_cache_in_context2(sql, params, table_name, "int", entityClass, SuidType.UPDATE)
            
            super().logsql("updateBy SQL:", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)
        except Exception as e: 
            raise BeeException(e) 
        finally:
            super().doBeforeReturnSimple()
            
    # since 1.6.0
    # * @param entity table's entity(do not allow null).
    # * <br>If the field of entity is not null or empty, it will be translate to field=value in where part.Other can define with condition.
    # def update3(self, entity, condition: Condition=None, *updateFields): 
    
    def create_table(self, entityClass, is_drop_exist_table = None):
        if is_drop_exist_table:
            sql0 = self.objToSQL.toDropTableSQL(entityClass)
            super().logsql("drop table SQL:", sql0)
            self.beeSql.modify(sql0)
        sql = self.objToSQL.toCreateSQL(entityClass)
        super().logsql("create table SQL:", sql)
        return self.beeSql.modify(sql)
    
    def index_normal(self, entity_class, fields, index_name = None): 
        prefix = "idx_"  
        index_type_tip = "normal"  
        index_type = ""  # normal will be empty  
        self._index(entity_class, fields, index_name, prefix, index_type_tip, index_type)  

    def unique(self, entity_class, fields, index_name = None): 
        prefix = "uie_"  
        index_type_tip = "unique"  
        index_type = "UNIQUE "
        self._index(entity_class, fields, index_name, prefix, index_type_tip, index_type)  

    def _index(self, entity_class, fields, index_name, prefix, index_type_tip, index_type): 
        index_sql = self.objToSQL.to_index_sql(entity_class, fields, index_name, prefix, index_type_tip, index_type)  
        self._index_modify(index_sql)  

    def _index_modify(self, index_sql): 
        super().logsql("create index SQL:", index_sql)  
        self.beeSql.modify(index_sql)
    
    def drop_index(self, entity_class, index_name = None):
        sql = self.objToSQL.to_drop_index_sql(entity_class, index_name)
        super().logsql("drop index SQL:", sql)
        self.beeSql.modify(sql)


# for custom SQL
# custom SQL do not support cache
class PreparedSql(AbstractCommOperate):
    
    """
    eg:
    """ 

    def select(self, sql, return_type_class, params = None, start = None, size = None):
        if not sql: 
            return None  
        if not return_type_class: 
            return None

        try:
            sql = self.__adjust_placeholder(sql)
            
            sql = SqlUtil.add_paging(sql, start, size)
            
            super().logsql("select SQL(PreparedSql):", sql)
            super().log_params(params)
            return self.beeSql.select(sql, return_type_class, params)
        except Exception as e: 
            raise BeeException(e)
        
    """
    eg:
      preparedSql=PreparedSql()
      entity_list =preparedSql.select_dict("SELECT * FROM orders WHERE name=#{name} and id=#{id} and name=#{name}", Orders, params_dict ={"name":"bee1","id":4})
    """ 

    def select_dict(self, sql, return_type_class, params_dict = None, start = None, size = None):
        params = None
        if params_dict:
            sql, params = SqlUtil.transform_sql(sql, params_dict)  
        return self.select(sql, return_type_class, params, start, size)
    
    """
    eg:
        sql = "update orders set name = ?, remark = ? where id = ?"
        params = ('bee130', 'test-update', 1)
        updateNum = preparedSql.modify(sql, params)
    """     

    # def modify(self, sql: str, params=None) -> int:
    def modify(self, sql, params = None): 
        try: 
            sql = self.__adjust_placeholder(sql)
            super().logsql("modify SQL(PreparedSql):", sql)
            super().log_params(params)
            return self.beeSql.modify(sql, params)  
        except Exception as e: 
            raise BeeException(e)
        
    def __adjust_placeholder(self, sql):
        placeholder = HoneyContext.get_placeholder()  # in python different db have diffent placeholder
        sql = sql.replace("%s", placeholder)
        sql = sql.replace("?", placeholder)
        return sql
    
    """
    eg:
        sql = "update orders set name = #{name}, remark = #{remark} where id = #{id}"
        params_dict={"id":1, "name":"newName","remark":"remark2"}
        updateNum = preparedSql.modify_dict(sql, params_dict)
    """        

    def modify_dict(self, sql, params_dict = None):
        params = None
        if params_dict:
            sql, params = SqlUtil.transform_sql(sql, params_dict)
        return self.modify(sql, params)
    
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
        
