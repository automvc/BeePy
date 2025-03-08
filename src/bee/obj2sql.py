from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.exception import SqlBeeException
from bee.name import NameCheckUtil
from bee.osql.const import DatabaseConst, SysConst
from bee.osql.logger import Logger
from bee.osql.sqlkeyword import K
from bee.paging import Paging
from bee.util import HoneyUtil

from bee.name.naming_handler import NamingHandler


class ObjToSQL:

    def toSelectSQL(self, entity):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_select_sql(table_name, classField, fieldAndValue)
    
    def toSelectSQLWithPaging(self, entity, start, size):
        sql, params = self.toSelectSQL(entity)
        
        paging = Paging()
        sql = paging.to_page_sql(sql, start, size)
        return sql, params
    
    def toUpdateSQL(self, entity):
        fieldAndValue = self.__getKeyValue(entity)
        pk = HoneyUtil.get_pk(entity)
        if pk is None:
            if SysConst.id in fieldAndValue:
                pk=SysConst.id 
            else:
                raise SqlBeeException("update by id, bean should has id field or need set the pk field name with __pk__")
                
        pkvalue = fieldAndValue.pop(pk, None)
        if pkvalue is None:
            raise SqlBeeException("the id/pk value can not be None")
            
        conditions = {pk:pkvalue}    
        
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
    
    def toInsertBatchSQL(self, entity_list): 
        table_name = HoneyUtil.get_table_name(entity_list[0])
        # fieldAndValue = self.__getKeyValue(entity_list[0])
        
        cls=type(entity_list[0])
        classField = HoneyUtil.get_class_field(cls)
        sql=self.__build_insert_batch_sql(table_name, classField)
        list_params= HoneyUtil.get_list_params(classField, entity_list)
        
        return sql, list_params
    
    def toSelectByIdSQL(self, entity):
        classField, condition = self._toById(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        
        return self.__build_select_sql(table_name, classField, condition)
    
    def toDeleteById(self, entity):
        _, condition = self._toById(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        
        return self.__build_delete_sql(table_name, condition)
    
    
    def _toById(self, entity):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        pk = HoneyUtil.get_pk(entity)
        if pk is None:
            if SysConst.id in fieldAndValue:
                pk = SysConst.id 
            else:
                raise SqlBeeException("by id, bean should has id field or need set the pk field name with __pk__")
                
        pkvalue = fieldAndValue.pop(pk, None)
        if pkvalue is None:
            raise SqlBeeException("the id/pk value can not be None")
            
        conditions = {pk:pkvalue}    
        return classField, conditions
    
    def toSelectFunSQL(self, entity, functionType, field_for_fun):
        fieldAndValue, _ = self.__getKeyValue_classField(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_select_fun_sql(table_name, functionType, field_for_fun, fieldAndValue)
    
    def __getKeyValue(self, entity):
        fieldAndValue, _ = self.__getKeyValue_classField(entity)
        return fieldAndValue
    
    #__  or _只是用于范围保护，转成sql时，将这两种前缀统一去掉
    def __getKeyValue_classField(self, entity):
        
        cls=type(entity)
        classField = HoneyUtil.get_class_field(cls)  # list
        fieldAndValue = HoneyUtil.get_obj_field_value(entity)  # dict
        
        classFieldAndValue = HoneyUtil.get_class_field_value(cls)
        
        # 获取去掉前缀的键    todo __ ??
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
        if not set_dict:
            raise SqlBeeException("Update SQL's set part is empty!")
        
        # if not conditions:  #还没有用到
        #     Logger.warn("Update SQL's where part is empty, would update all records!")
        
        set_dict2 = self.__toColumns_with_dict(set_dict)
        conditions2 = self.__toColumns_with_dict(conditions)
        
        ph=self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            updateSet = ', '.join(f"{key} = {ph}{key}" for key in set_dict2.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in conditions2.keys())
        else:
            updateSet = ', '.join(f"{key} = {ph}" for key in set_dict2.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in conditions2.keys())
        
        # sql = f"UPDATE {table_name} SET {updateSet} WHERE {condition_str}"
        sql = f"{K.update()} {table_name} {K.set()} {updateSet} {K.where()} {condition_str}"
        params = list(set_dict2.values()) + list(conditions2.values())
        return sql, params
    
    
    def __build_insert_sql(self, table_name, data):
        if not data:
            raise SqlBeeException("insert column and value is empty!")
        
        data2 = self.__toColumns_with_dict(data)
        
        ph=self.__getPlaceholder()
        columns = ', '.join(data2.keys())
        if self.__getPlaceholderType() == 3:
            placeholders = ', '.join(f" {ph}{key}" for key in data2.keys())
        else:
            placeholders = ', '.join(f"{ph}" for _ in data2) #TODO
        sql = f"{K.insert()} {K.into()} {table_name} ({columns}) {K.values()} ({placeholders})"
        return sql, list(data2.values())
    
    def __build_insert_batch_sql(self, table_name, classField):
        if not classField:
            raise SqlBeeException("column list is empty!")
        
        columns=self.__toColumns(classField)
        
        ph=self.__getPlaceholder()
        columnsStr = ', '.join(columns)
        if self.__getPlaceholderType() == 3:
            placeholders = ', '.join(f" {ph}{item}" for item in classField)
        else:
            placeholders = ', '.join(f"{ph}" for _ in classField)
        sql = f"{K.insert()} {K.into()} {table_name} ({columnsStr}) {K.values()} ({placeholders})"
        return sql
    
    def __toColumns_with_dict(self, kv):
        return {NamingHandler.toColumnName(k):v for k, v in kv.items()}

    def __build_where_condition(self, conditions):
        conditions2 = self.__toColumns_with_dict(conditions)
        
        ph = self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in conditions2.keys())
        else:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in conditions2.keys())
        return condition_str
    
    def __toColumns(self, classField):
        return [NamingHandler.toColumnName(field) for field in classField]
    
    def __build_select_sql(self, table_name, classField, conditions=None):
        if not classField:
            raise SqlBeeException("column list is empty!")
        
        columns=self.__toColumns(classField)
        # sql = f"SELECT * FROM {table_name}"
        # sql = f"SELECT {', '.join(classField)} FROM {table_name}"
        sql = f"{K.select()} {', '.join(columns)} {K.from_()} {table_name}"
        
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
        else:
            return 0
        
    def __build_select_fun_sql(self, table_name, functionType, field_for_fun, conditions=None):
        column_for_fun=NamingHandler.toColumnName(field_for_fun)
        
        # sql = f"SELECT count() FROM {table_name}"
        sql = f"{K.select()} {functionType.get_name()}({column_for_fun}) {K.from_()} {table_name}"
        
        #where part
        params = []
        if conditions:
            condition_str=self.__build_where_condition(conditions)
            sql += f" {K.where()} {condition_str}"
            params = list(conditions.values())
        return sql, params
    
    #ddl
    def toCreateSQL(self, entityClass):
        classField = HoneyUtil.get_class_field(entityClass)  # list
        # print(classField)
        # fieldAndValue, classField = self.__getKeyValue_classField(entity)
        pk = HoneyUtil.get_pk_by_class(entityClass)
        table_name = HoneyUtil.get_table_name_by_class(entityClass)
        if pk is None:
            if SysConst.id in classField:
                pk = SysConst.id 
            else:
                Logger.warn("There are no primary key when create table: " + table_name)
                
        # print(pk) # bug
        # classField.remove(pk)
        hasPk = False
        if pk in classField: 
            classField.remove(pk)
            hasPk = True
        
        classField = self.__toColumns(classField)
        
        field_type = "VARCHAR(255)"  # 假设所有非主键字段都是 VARCHAR(255)   TODO
    
        pk_statement = ""
        # 创建主键字段语句  
        if hasPk:
            pk = NamingHandler.toColumnName(pk)
            pk_statement = self.generate_pk_statement(pk)
        
        # 创建其他字段语句  
        fields_statement = [f"{field} {field_type}" for field in classField]  
        
        if hasPk:
            # 合并主键和字段  
            all_fields_statement = [pk_statement] + fields_statement  
        else:
            all_fields_statement = fields_statement
        
        # 生成完整的 CREATE TABLE 语句  
        create_sql = f"CREATE TABLE {table_name} (\n    " + ',\n    '.join(all_fields_statement) + "\n);"  
        return create_sql
    
    def generate_pk_statement(self, pk): 
        honeyConfig = HoneyConfig()
        dbName = honeyConfig.get_dbName()
        if dbName == DatabaseConst.MYSQL.lower(): 
            return f"{pk} INT PRIMARY KEY AUTO_INCREMENT NOT NULL"  
        elif dbName == DatabaseConst.SQLite.lower(): 
            return f"{pk} INTEGER PRIMARY KEY"  # 自动增长  
        elif dbName == DatabaseConst.ORACLE.lower(): 
            return f"{pk} NUMBER PRIMARY KEY"  
        elif dbName == DatabaseConst.PostgreSQL.lower(): 
            return f"{pk} SERIAL PRIMARY KEY"  
        else: 
            raise ValueError(f"Unsupported database type: {dbName}")  

    def toDropTableSQL(self, entityClass):
        honeyConfig = HoneyConfig()
        table_name = HoneyUtil.get_table_name_by_class(entityClass)
        dbName = honeyConfig.get_dbName()
        if dbName == DatabaseConst.ORACLE.lower() or dbName == DatabaseConst.SQLSERVER.lower(): 
            sql0 = "DROP TABLE " + table_name;
        else:
            sql0 = "DROP TABLE IF EXISTS " + table_name;
        return sql0
    
    def to_index_sql(self, entity_class, fields, index_name, prefix, index_type_tip, index_type): 
        if not fields: 
            raise ValueError(f"Create {index_type_tip} index, the fields can not be empty!")  
        
        NameCheckUtil.check_field(fields)  
        table_name = HoneyUtil.get_table_name_by_class(entity_class)
        columns = self.transfer_field(fields, entity_class)  

        if not index_name: 
            index_name = f"{prefix}{table_name}_{columns.replace(',', '_')}"  
        else: 
            NameCheckUtil.check_field(index_name)

        index_sql = f"CREATE {index_type}INDEX {index_name} ON {table_name} ({columns})"  
        return index_sql 
    
    def transfer_field(self, fields, entity_class): 
        # 根据实际的实体类转换字段名  
        # return fields  # 这里简单返回，可以根据需求进行字段转换   TODO
        return NamingHandler.toColumnName(fields)

    def to_drop_index_sql(self, entity_class, index_name): 
        table_name = HoneyUtil.get_table_name_by_class(entity_class)
        honeyConfig = HoneyConfig()
        dbName = honeyConfig.get_dbName()

        if index_name: 
            if dbName == DatabaseConst.SQLSERVER.lower(): 
                drop_sql = "DROP INDEX table_name.index_name"  
            elif dbName == DatabaseConst.ORACLE.lower() or dbName == DatabaseConst.SQLite.lower() or dbName == DatabaseConst.DB2.lower():
                drop_sql = "DROP INDEX index_name" 
            elif dbName == DatabaseConst.MYSQL.lower() or dbName == DatabaseConst.MsAccess.lower(): 
                drop_sql = "DROP INDEX index_name ON table_name"  
            else: 
                drop_sql = "DROP INDEX index_name"  

            return drop_sql.replace("table_name", table_name).replace("index_name", index_name)  
        else: 
            return f"DROP INDEX ALL ON {table_name}"  
        
