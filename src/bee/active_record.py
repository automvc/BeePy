from bee.api import Suid, SuidRich
from bee.condition import Condition
from bee.bee_enum import FunctionType


class BaseMode:
    
    def __init__(self):
        self.__suid = Suid()
        self.__suidRich = SuidRich()
        
    def update(self): 
        '''
        According to entity object update record(update record by id).This method just has id field to SQL where expression.
        table's entity(do not allow null);id is where condition,do not allow null.<br>
        The entity corresponding to table and can not be null. <br>
        The ID field of entity cannot be null and as filter condition. <br>
        The not null and not empty field will update to database except ID.
        :return: the numbers of update records successfully, if fails,return integer less than 0.
        '''
        return self.__suid.update(self)
        
    def insert(self):
        '''
        According to entity object insert record. 
        The entity corresponding to table and can not be null. <br>
        The not null and not empty field will insert to database.<br>
        :return: the numbers of insert records successfully, if fails,return integer less than 0.
        '''
        return self.__suid.insert(self) 
        
    def select(self, condition: Condition = None): 
        '''
        Select the records according to entity and condition.<br>
        <B>since  1.6.0</B><br>
        :param condition: If the field of entity is not null or empty, it will be translate to field=value.<br>
        Other can define with condition. <br>
        :return: list which contains more than one entity.<br>
        '''
        return self.__suid.select(self, condition)
        
    def delete(self, condition: Condition = None): 
        '''
        Delete the records according to entity and condition.<br>
        <B>since  1.6.0</B>
        :param condition: If the field of entity is not null or empty, it will be translate to field=value.Other can define with condition. 
        :return: the number of deleted record(s) successfully, if fails,return integer less than 0.
        '''
        return self.__suid.delete(self, condition)
    
    ################ suidRich
    def select_paging(self, start, size, *selectFields):
        '''
        Just select some fields,and can specify page information.
        :param start: start index,min value is 0 or 1(eg:MySQL is 0,Oracle is 1).
        :param size: fetch result size (>0).
        :param selectFields: select fields, if more than one,separate with comma in one selectField parameter or use variable parameter.
        :return: list which contains more than one entity.
        '''
        return self.__suidRich.select_paging(self, start, size, *selectFields)
        
    # def insert_batch(self, entity_list):
    #     '''
    #     Insert records by batch type.
    #     :param entity_list: table's entity list(do not allow null).<br>
    #     :return: the number of inserted record(s) successfully.
    #     '''
    #     return self.__suidRich.insert_batch(entity_list)
    
    def select_first(self):
        '''
        select the first record.
        :return: return the first record
        '''
        return self.__suidRich.select_first(self)
    
    def select_by_id(self, *ids):
        '''
        Select record by id.
        :param  id: value of entity's id field. 
        :return: return one entity which owns this id.
        '''
        return self.__suidRich.select_by_id(type(self), *ids) 
    
    def delete_by_id(self, *ids):
        '''
        Delete record by id.
        :param  ids: value of entity's id field.
        :return: the number of deleted record(s) successfully,if fails, return integer less than 0.
        '''
        return self.__suidRich.delete_by_id(type(self), *ids)
    
    def select_fun(self, functionType:FunctionType, field_for_fun):
        '''
        Select result with one function,Just select one function.
        :param functionType: MAX,MIN,SUM,AVG,COUNT
        :param field_for_fun: field for function.
        :return: one function result.<br>
        <br>If the result set of statistics is empty,the count return 0,the other return empty string.
        '''
        return self.__suidRich.select_fun(self, functionType, field_for_fun)
    
    def count(self):
        '''
        total number of statistical records.
        :return: total number of records that satisfy the condition.
        '''
        return self.__suidRich.count(self)
    
    def exist(self):
        '''
        Check whether the entity corresponding record exist
        :return: true,if have the record;or return false.
        '''
        return self.__suidRich.exist(self)
    
    def updateBy(self, condition: Condition = None, *whereFields):
        '''
        Update record according to whereFields.
        :param condition: Condition as filter the record.
        :param whereFields: As a field list of where part in SQL, multiple fields can separated by commas in one 
        <br>whereField parameter or use variable parameter (the fields in the list will be used as where filter)
        <br>But if id's value is null can not as filter.
        <br>Notice:the method op of condition also maybe converted to the where expression.
        :return: the numbers of update record(s) successfully,if fails, return integer less than 0.
        '''
        return self.__suidRich.updateBy(self, condition, *whereFields)
    
