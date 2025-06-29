from typing import overload

from bee.condition import Condition
from bee.bee_enum import FunctionType

from bee.osql.engine import ObjSQL, ObjSQLRich, PreparedSqlLib


class Suid:
    '''
    Database operation: Suid (select,update,insert,delete),<br>
    the null and empty string are not handled by default.<br>
    '''
    
    def __init__(self):
        self.__suid = ObjSQL()
        
    @overload
    def select(self, entity):
        ...
    
    def update(self, entity): 
        '''
        According to entity object update record(update record by id).This method just has id field to SQL where expression.
        table's entity(do not allow null);id is where condition,do not allow null.<br>
        The entity corresponding to table and can not be null. <br>
        The ID field of entity cannot be null and as filter condition. <br>
        The not null and not empty field will update to database except ID.
        :param entity: table's entity(do not allow null).<br>
        The ID field of entity cannot be null and as filter condition. <br>
        :return: the numbers of update records successfully, if fails,return integer less than 0.
        '''
        return self.__suid.update(entity)
        
    def insert(self, entity):
        '''
        According to entity object insert record. 
        :param entity: table's entity(do not allow null).<br>
        The entity corresponding to table and can not be null. <br>
        The not null and not empty field will insert to database.<br>
        :return: the numbers of insert records successfully, if fails,return integer less than 0.
        '''
        return self.__suid.insert(entity) 
        
    @overload
    def delete(self, entity):
        ...
        
    def select(self, entity, condition: Condition = None): 
        '''
        Select the records according to entity and condition.<br>
        <B>since  1.6.0</B><br>
        :param entity: table's entity(do not allow null).<br>
        :param condition: If the field of entity is not null or empty, it will be translate to field=value.<br>
        Other can define with condition. <br>
        :return: list which contains more than one entity.<br>
        '''
        return self.__suid.select(entity, condition)
        
    def delete(self, entity, condition: Condition = None): 
        '''
        Delete the records according to entity and condition.<br>
        <B>since  1.6.0</B>
        :param entity: table's entity(do not allow null).
        :param condition: If the field of entity is not null or empty, it will be translate to field=value.Other can define with condition. 
        :return: the number of deleted record(s) successfully, if fails,return integer less than 0.
        '''
        return self.__suid.delete(entity, condition)
    

class SuidRich(Suid):
    '''
    Database operation: Suid (select,update,insert,delete),
    it supports more parameters than Suid.
    
    The SQL UPDATE statement consists of two parts: set and where. SuidRich specifies one of them 
    <br>and tries to use the default implementation method for the other. 
    <br>Therefore, the update method is divided into two parts:
    
    in the <B>updateBy</B> method, string whereFields (if has) can indicate the field used for WHERE in SQL.
    <br>When whereFields is specified, fields that are not in whereFields will default.
    <br>Convert to the set part of SQL UPDATE statement (null and empty strings are filtered by default).
    <br>If the value of an attribute of the same entity is used in the where part, it is meaningless to use it 
    <br>in the update set part (because their values are the same at this time)
    <br>However, it can be set by using the set(String fieldName, Number num) and other methods; 
    <br>The method set,setMultiply,setAdd,setWithField of condition is processed before processing the where field, 
    <br>so it is not affected by the specified where condition field
    
    The fields set by the Condition of the updateBy methods will be parsed, which is not affected by the updateFields 
    <br>parameter and the whereFields parameter.
    '''
    
    def __init__(self):
        self.__suidRich = ObjSQLRich()
    
    @overload
    def select_paging(self, entity, start, size): 
        ...
    
    def select_paging(self, entity, start, size, *selectFields):
        '''
        Just select some fields,and can specify page information.
        :param entity: table's entity(do not allow null).
        :param start: start index,min value is 0 or 1(eg:MySQL is 0,Oracle is 1).
        :param size: fetch result size (>0).
        :param selectFields: select fields, if more than one,separate with comma in one selectField parameter or use variable parameter.
        :return: list which contains more than one entity.
        '''
        return self.__suidRich.select_paging(entity, start, size, *selectFields)
        
    def insert_batch(self, entity_list):
        '''
        Insert records by batch type.
        :param entity_list: table's entity list(do not allow null).<br>
        :return: the number of inserted record(s) successfully.
        '''
        return self.__suidRich.insert_batch(entity_list)
    
    def select_first(self, entity):
        '''
        select the first record.
        :param entity: table's entity(do not allow null).
        :return: return the first record
        '''
        return self.__suidRich.select_first(entity)
    
    def select_by_id(self, entity_class, *ids):
        '''
        Select record by id.
        :param entity_class: table's entity class(do not allow null).
        :param  id: value of entity's id field. 
        :return: return one entity which owns this id.
        '''
        return self.__suidRich.select_by_id(entity_class, *ids) 
    
    def delete_by_id(self, entity_class, *ids):
        '''
        Delete record by id.
        :param entity_class: table's entity class(do not allow null).
        :param  ids: value of entity's id field.
        :return: the number of deleted record(s) successfully,if fails, return integer less than 0.
        '''
        return self.__suidRich.delete_by_id(entity_class, *ids)
    
    def select_fun(self, entity, functionType:FunctionType, field_for_fun):
        '''
        Select result with one function,Just select one function.
        :param entity: table's entity(do not allow null).
        :param functionType: MAX,MIN,SUM,AVG,COUNT
        :param field_for_fun: field for function.
        :return: one function result.<br>
        <br>If the result set of statistics is empty,the count return 0,the other return empty string.
        '''
        return self.__suidRich.select_fun(entity, functionType, field_for_fun)
    
    def count(self, entity):
        '''
        total number of statistical records.
        :param entity:  table's entity(do not allow null).
        :return: total number of records that satisfy the condition.
        '''
        return self.__suidRich.count(entity)
    
    def exist(self, entity):
        '''
        Check whether the entity corresponding record exist
        :param entity: table's entity(do not allow null).
        :return: true,if have the record;or return false.
        '''
        return self.__suidRich.exist(entity)
    
    def updateBy(self, entity, condition: Condition = None, *whereFields):
        '''
        Update record according to whereFields.
        :param entity: table's entity(do not allow null).
        <br>Fields that are not specified as whereFields, as part of the set(only non empty and non null fields 
        <br>are processed by default).
        :param condition: Condition as filter the record.
        :param whereFields: As a field list of where part in SQL, multiple fields can separated by commas in one 
        <br>whereField parameter or use variable parameter (the fields in the list will be used as where filter)
        <br>But if id's value is null can not as filter.
        <br>Notice:the method op of condition also maybe converted to the where expression.
        :return: the numbers of update record(s) successfully,if fails, return integer less than 0.
        '''
        return self.__suidRich.updateBy(entity, condition, *whereFields)
    
    def create_table(self, entity_class, is_drop_exist_table = None):
        '''
        According to the database table generated by Bean, Bean does not need to configure 
        <br>too much field information. This method only considers the general situation, and is not 
        <br>recommended if there are detailed requirements.
        :param entity_class:Class table's entity_class(do not allow null).
        :param is_drop_exist_table: whether drop the exist table before create
        :return: flag whether create successfully.
        '''
        return self.__suidRich.create_table(entity_class, is_drop_exist_table)
    
    def index_normal(self, entity_class, fields, index_name = None): 
        '''
        create normal index
        :param entity_class: class type of entity.
        :param fields: the fields of entity.
        :param index_name: index name
        '''
        return self.__suidRich.index_normal(entity_class, fields, index_name)
    
    def unique(self, entity_class, fields, index_name = None): 
        '''
        create unique index 
        :param entity_class: class type of entity.
        :param fields: the fields of entity.
        :param index_name: index name
        '''
        return self.__suidRich.unique(entity_class, fields, index_name)
    
    def drop_index(self, entity_class, index_name = None):
        '''
        drop index
        :param entity_class: class type of entity.
        :param index_name: index name
        '''
        return self.__suidRich.drop_index(entity_class, index_name)
   
    
class PreparedSql:
    '''
    Support sql string with placeholder.The sql statement is really DB's grammar,not object oriented type.
    <br>Support placeholder or #{para} or #{para%} or #{%para} or #{%para%},
    <br>can prevent SQL injection attacks through Preparedstatement
    <p>If possible, it is recommended to use object-oriented operation methods, such as Suid and SuidRich. 
    <br>It can use Bee cache to achieve higher query efficiency.
    '''
    
    def __init__(self):
        self.__preparedSql = PreparedSqlLib()
    
    def select(self, sql, return_type_class, params = None, start = None, size = None):
        '''
        Select record(s) via the placeholder(?) statement.
        <br>eg: select * from orders where userid=?
        :param sql: SQL select statement which use placeholder
        :param return_type_class: class type for return
        :param params: list type params for placeholder
        :param start: Start index,min value is 0 or 1(eg:MySQL is 0,Oracle is 1).
        :param size: Fetch result size (>0).  
        :return: list which element type is same as return_type_class.
        '''
        return self.__preparedSql.select(sql, return_type_class, params, start, size)
    
    def select_dict(self, sql, return_type_class, params_dict = None, start = None, size = None):
        '''
        Select record(s) via the placeholder(?) statement.
        <br>eg: select * from orders where userid=?
        :param sql: SQL select statement which use placeholder
        :param return_type_class: class type for return
        :param params_dict: dict type params for placeholder
        :param start: start index, min value is 0 or 1(eg:MySQL is 0,Oracle is 1).
        :param size: fetch result size (>0).  
        :return: list which element type is same as return_type_class.
        '''
        return self.__preparedSql.select_dict(sql, return_type_class, params_dict, start, size)          
    
    def modify(self, sql, params = None): 
        '''
        Modify database records with update, insert or delete statement.
        It is not recommended because the framework does not know what table has been changed, 
        <br>which will affect the correctness of the cache and cause the risk of inaccurate cache data.
        :param sql: SQL statement which use placeholder.
        :param params: list type params for placeholder
        :return: the number of affected successfully records. 
        '''
        return self.__preparedSql.modify(sql, params)
    
    def modify_dict(self, sql, params_dict = None):
        '''
        Modify database records with update, insert or delete statement.
        It is not recommended because the framework does not know what table has been changed, 
        <br>which will affect the correctness of the cache and cause the risk of inaccurate cache data.
        :param sql: SQL statement which use placeholder.
        :param params_dict: dict type params for placeholder
        :return: the number of affected successfully records. 
        '''
        return self.__preparedSql.modify_dict(sql, params_dict)
        
