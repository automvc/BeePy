from bee import SqlUtil
from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.exception import SqlBeeException, ParamBeeException
from bee.name import NameCheckUtil
from bee.name.naming_handler import NamingHandler
from bee.osql.const import DatabaseConst, SysConst
from bee.osql.enum import SuidType
from bee.osql.logger import Logger
from bee.osql.sqlkeyword import K
from bee.util import HoneyUtil

from bee.condition import Condition


class ObjToSQL:

    def toSelectSQL(self, entity):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_select_sql(table_name, classField, fieldAndValue)
    
    def toSelectSQL2(self, entity, condition: Condition):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_select_sql2(table_name, classField, fieldAndValue, condition)
    
    def toSelectSQLWithPaging(self, entity, start, size):
        sql, params = self.toSelectSQL(entity)
        
        sql = SqlUtil.add_paging(sql, start, size)
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
    
    def toUpdateBySQL2(self, entity, condition, whereFields):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        ext=list(set(whereFields) - set(classField))
        if ext:
            raise ParamBeeException("some fields in whereFields not in bean: ", ext)
        
        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_update_by_sql2(table_name, fieldAndValue, condition, whereFields)
    
    def toInsertSQL(self, entity):
        table_name = HoneyUtil.get_table_name(entity)
        fieldAndValue = self.__getKeyValue(entity)
        return self.__build_insert_sql(table_name, fieldAndValue)
    
    
    def toDeleteSQL(self, entity):
        table_name = HoneyUtil.get_table_name(entity)
        fieldAndValue = self.__getKeyValue(entity)
        return self.__build_delete_sql(table_name, fieldAndValue)
    
    def toDeleteSQL2(self, entity, condition):
        table_name = HoneyUtil.get_table_name(entity)
        fieldAndValue = self.__getKeyValue(entity)
        return self.__build_delete_sql2(table_name, fieldAndValue, condition)
    
    def toInsertBatchSQL(self, entity_list): 
        table_name = HoneyUtil.get_table_name(entity_list[0])
        # fieldAndValue = self.__getKeyValue(entity_list[0])
        
        cls=type(entity_list[0])
        classField = HoneyUtil.get_class_field(cls)
        sql=self.__build_insert_batch_sql(table_name, classField)
        list_params= HoneyUtil.get_list_params(classField, entity_list)
        
        return sql, list_params
    
    def toSelectByIdSQL(self, entity_class, length):
        classField = HoneyUtil.get_class_field(entity_class)  # list 
        where_condition_str = self._toWhereById(entity_class, length)
    
        table_name = HoneyUtil.get_table_name_by_class(entity_class)
    
        return self.__build_select_by_id_sql(table_name, classField, where_condition_str)
    
    def _toWhereById(self, entity_class, length):
        
        pk = HoneyUtil.get_pk_by_class(entity_class)
        if pk is None:
            raise SqlBeeException("by id, bean should has id field or need set the pk field name with __pk__")
        
        pk = NamingHandler.toColumnName(pk)
        
        ph = self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            condition_str = f" {K.or_()} ".join([f"{pk} = {ph}{pk}"] * length)
        else:
            condition_str = f" {K.or_()} ".join([f"{pk} = {ph}" ] * length)
        
        return f" {K.where()} {condition_str}"
    
    def toDeleteById(self, entity_class, length):
        where_condition_str = self._toWhereById(entity_class, length)
        table_name = HoneyUtil.get_table_name_by_class(entity_class)
        return self.__build_delete_by_id_sql(table_name, where_condition_str)
    
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

    #updateById
    def __build_update_sql(self, table_name, set_dict, entityFilter):
        # entityFilter just pk 
        if not set_dict:
            raise SqlBeeException("Update SQL's set part is empty!")
        
        # if not entityFilter:  #还没有用到
        #     Logger.warn("Update SQL's where part is empty, would update all records!")
        
        set_dict2 = self.__toColumns_with_dict(set_dict)
        conditions2 = self.__toColumns_with_dict(entityFilter)
        
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

    def __build_where_condition(self, entityFilter):
        entityFilter2 = self.__toColumns_with_dict(entityFilter)
        
        ph = self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in entityFilter2.keys())
        else:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in entityFilter2.keys())
        return condition_str
    
    def __toColumns(self, classField):
        return [NamingHandler.toColumnName(field) for field in classField]
    
    def __build_select_sql(self, table_name, classField, entityFilter=None):
        if not classField:
            raise SqlBeeException("column list is empty!")
        
        columns=self.__toColumns(classField)
        # sql = f"SELECT * FROM {table_name}"
        # sql = f"SELECT {', '.join(classField)} FROM {table_name}"
        sql = f"{K.select()} {', '.join(columns)} {K.from_()} {table_name}"
        
        #where part
        params = []
        if entityFilter:
            condition_str=self.__build_where_condition(entityFilter)
            sql += f" {K.where()} {condition_str}"
            params = list(entityFilter.values())
        return sql, params
    
    def __build_select_sql2(self, table_name, classField, entityFilter=None, condition=None):
        
        if condition:
            conditionStruct=condition.parseCondition()
            selectFields=conditionStruct.selectFields
        
        if not selectFields and not classField:
            raise SqlBeeException("column list is empty!")
        
        if selectFields:
            columns=self.__toColumns(selectFields) # TODO
        else:
            columns=self.__toColumns(classField)
            
        sql = f"{K.select()} {', '.join(columns)} {K.from_()} {table_name}"
        
        #where part
        params = []
        if entityFilter:
            condition_str=self.__build_where_condition(entityFilter)
            sql += f" {K.where()} {condition_str}"
            params = list(entityFilter.values())
            
        if conditionStruct:
            sql,params=self.__appendWhere(sql, params, entityFilter, conditionStruct)
            start = conditionStruct.start
            size = conditionStruct.size
            if start or size:
                sql = SqlUtil.add_paging(sql, start, size)
            if conditionStruct.has_for_update:
                sql += " " + K.for_update()
            
        return sql, params
    
    def __appendWhere(self,sql,params,entityFilter,conditionStruct):
        if conditionStruct:
            condition_where=conditionStruct.where
            if condition_where:
                values=conditionStruct.values
                if entityFilter:
                    sql += " "+ K.and_()
                else:
                    sql +=" "+ K.where()
                sql +=" "+condition_where
                params = params + values
        return sql,params
    
    def __build_delete_sql2(self, table_name, entityFilter, condition=None):
        sql = f"{K.delete()} {K.from_()} {table_name}"
        params = []
        if entityFilter:
            condition_str=self.__build_where_condition(entityFilter)
            sql += f" {K.where()} {condition_str}"
            params = list(entityFilter.values())
            
        if condition:
            condition.suidType(SuidType.DELETE)
            conditionStruct=condition.parseCondition()
            sql,params=self.__appendWhere(sql, params, entityFilter, conditionStruct)
            
        return sql, params
    
    def __build_update_by_sql2(self, table_name, entityFilter, condition, whereFields):
        
        where_dict = {}  
        set_dict = {}  
        for key, value in entityFilter.items():  
            if key in whereFields:  
                where_dict[key] = value  
            else:  
                set_dict[key] = value
                
        if not set_dict:
            raise SqlBeeException("UpdateBy SQL's set part is empty!")
        
        null_value_filter = set(whereFields) - set(where_dict)
        
        if condition:
            condition.suidType(SuidType.UPDATE)
            conditionStruct=condition.parseCondition()
            where=conditionStruct.where
            if not where_dict and not where:
                Logger.warn("Update SQL's where part is empty, would update all records!")
        
        set_dict2 = self.__toColumns_with_dict(set_dict)
        conditions2 = self.__toColumns_with_dict(where_dict)
        
        ph=self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            updateSet = ', '.join(f"{key} = {ph}{key}" for key in set_dict2.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in conditions2.keys())
        else:
            updateSet = ', '.join(f"{key} = {ph}" for key in set_dict2.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in conditions2.keys())
        
        if null_value_filter:
            no_value_filter2 = self.__toColumns(null_value_filter)
            if condition_str:
                condition_str+=" " +{K.and_()}
            condition_str += f" {K.and_()} ".join(f"{key} {K.isnull()}" for key in no_value_filter2)
        
        if condition_str:
            sql = f"{K.update()} {table_name} {K.set()} {updateSet} {K.where()} {condition_str}"
        else:
            sql = f"{K.update()} {table_name} {K.set()} {updateSet}" 
        params = list(set_dict2.values()) + list(conditions2.values())
        
        if where:    
            sql,params=self.__appendWhere(sql, params, whereFields, conditionStruct)
            
        return sql, params
    
    
    def __build_select_by_id_sql(self, table_name, classField, where_condition_str):
        if not classField:
            raise SqlBeeException("column list is empty!")
        
        columns = self.__toColumns(classField)
        sql = f"{K.select()} {', '.join(columns)} {K.from_()} {table_name}"
        return sql + where_condition_str

    def __build_delete_sql(self, table_name, entityFilter):
        return self.__build_delete_sql2(table_name, entityFilter, None)
    
    def __build_delete_by_id_sql(self, table_name, where_condition_str):
        sql = f"{K.delete()} {K.from_()} {table_name}"
        return sql + where_condition_str
    
    
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
        
