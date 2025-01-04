from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.key import Key
from bee.osql.const import DatabaseConst
from bee.osql.logger import Logger
from bee.osql.sqlkeyword import K
from bee.paging import Paging
from bee.util import HoneyUtil


class ObjToSQL:

    def toSelectSQL(self, entity):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_select_sql(table_name, classField, fieldAndValue);
    
    def toSelectSQLWithPaging(self, entity, start, size):
        sql, params = self.toSelectSQL(entity)
        
        paging = Paging()
        sql = paging.to_page_sql(sql, start, size)
        return sql, params
    
    def toUpdateSQL(self, entity):
        fieldAndValue = self.__getKeyValue(entity)
        pk = HoneyUtil.get_pk(entity)
        if pk is None:
            if not Key.id in fieldAndValue:
            # if not "id" in fieldAndValue:
                Logger.info("update by id,bean has id field or need set the pk field name with __pk__")  # TODO throw exception    
            else:
                idvalue = fieldAndValue.get(Key.id, None)
                if idvalue is None:
                    Logger.info("the id value can not be None")
                else:
                    pk = Key.id
            
        conditions = {pk:fieldAndValue.pop(pk)}    
    
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_update_sql(table_name, fieldAndValue, conditions)
    
        
    def toInsertSQL(self, entity):
        table_name = HoneyUtil.get_table_name(entity)
        fieldAndValue = self.__getKeyValue(entity)
        return self.__build_insert_sql(table_name, fieldAndValue)
    
    
    def toDeleteSQL(self, entity):
        table_name = HoneyUtil.get_table_name(entity)
        fieldAndValue = self.__getKeyValue(entity)
        return self.__build_delete_sql(table_name, fieldAndValue)
    
    def __getKeyValue(self, entity):
        fieldAndValue, _ = self.__getKeyValue_classField(entity)
        return fieldAndValue
    
    #__  or _只是用于范围保护，转成sql时，将这两种前缀统一去掉
    def __getKeyValue_classField(self, entity):
        
        cls=type(entity)
        classField = HoneyUtil.get_class_field(cls)  # list
        fieldAndValue = HoneyUtil.get_obj_field_value(entity)  # dict
        
        classFieldAndValue = HoneyUtil.get_class_field_value(cls)
        
        # 获取去掉前缀的键    TODO __ ??
        # fieldAndValue = {key.lstrip('_'): value for key, value in fieldAndValue.items()} 
        
        fieldAndValue = HoneyUtil.remove_prefix(fieldAndValue)
        
        objKey = fieldAndValue.keys()
        
        set1 = set(classField)
        set2 = set(objKey)  # list转set 顺序会乱了
        
        setExt = set2 - set1
        
        # 默认删除动态加的属性
        for k in setExt:
            fieldAndValue.pop(k, None)
       
        # 若对象的属性的值是None，则使用类级别的
        for name, value in fieldAndValue.items():
            if value is None:
                fieldAndValue[name] = classFieldAndValue[name]
        
        # 当对象的属性没有相应的值，而类的属性有，则使用类级的属性
        for name, value in classFieldAndValue.items():
            if value is not None and fieldAndValue.get(name, None) is None:
                fieldAndValue[name] = value

        #排除value为None的项
        fieldAndValue = {key: value for key, value in fieldAndValue.items() if value is not None}
        
        return  fieldAndValue, classField
    
    def __getPlaceholder(self):
        return HoneyContext.get_placeholder()
    

    def __build_update_sql(self, table_name, set_dict, conditions):
        ph=self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            updateSet = ', '.join(f"{key} = {ph}{key}" for key in set_dict.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in conditions.keys())
        else:
            updateSet = ', '.join(f"{key} = {ph}" for key in set_dict.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in conditions.keys())
        
        # sql = f"UPDATE {table_name} SET {updateSet} WHERE {condition_str}"
        sql = f"{K.update()} {table_name} {K.set()} {updateSet} {K.where()} {condition_str}"
        params = list(set_dict.values()) + list(conditions.values())
        return sql, params
    
    
    def __build_insert_sql(self, table_name, data):
        ph=self.__getPlaceholder()
        columns = ', '.join(data.keys())
        if self.__getPlaceholderType() == 3:
            placeholders = ', '.join(f" {ph}{key}" for key in data.keys())
        else:
            placeholders = ', '.join(f"{ph}" for _ in data)
        sql = f"{K.insert()} {K.into()} {table_name} ({columns}) {K.values()} ({placeholders})"
        return sql, list(data.values())

    def __build_where_condition(self, conditions):
        ph=self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in conditions.keys())
        else:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in conditions.keys())
        return condition_str
    
    def __build_select_sql(self, table_name, classField, conditions=None):
        # sql = f"SELECT * FROM {table_name}"
        # sql = f"SELECT {', '.join(classField)} FROM {table_name}"
        sql = f"{K.select()} {', '.join(classField)} {K.from_()} {table_name}"
        
        #where part
        params = []
        if conditions:
            condition_str=self.__build_where_condition(conditions)
            sql += f" {K.where()} {condition_str}"
            params = list(conditions.values())
        return sql, params
    

    def __build_delete_sql(self, table_name, conditions):

        sql = f"{K.delete()} {K.from_()} {table_name}"
        params = []
        if conditions:
            condition_str=self.__build_where_condition(conditions)
            sql += f" {K.where()} {condition_str}"
            params = list(conditions.values())
        return sql, params
    
    def __get_dbName(self):
        honeyConfig=HoneyConfig()
        return honeyConfig.get_dbName()
    
    def __getPlaceholderType(self):
        
        # sql = "SELECT * FROM employees WHERE employee_id = :emp_id"
        # cursor.execute(sql, emp_id=emp_id)  
        # sql = "INSERT INTO employees (employee_id, employee_name, salary) VALUES (:emp_id, :emp_name, :emp_salary)"  
        # cursor.execute(sql, emp_id=emp_id, emp_name=emp_name, emp_salary=emp_salary)
        if DatabaseConst.ORACLE.lower() == self.__get_dbName():
            return 3
