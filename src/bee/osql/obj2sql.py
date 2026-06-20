from typing import List

from bee.bee_enum import SuidType, JoinType, LocalType
from bee.condition import Condition
from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.exception import SqlBeeException, ParamBeeException
from bee.name import NameCheckUtil
from bee.name.naming_handler import NamingHandler
from bee.osql import SqlUtil
from bee.osql.const import DatabaseConst, SysConst
from bee.osql.logger import Logger
from bee.osql.sqlkeyword import K

from bee.osql.parsesql_helper import ParseSqlHelper
from bee.osql.util import HoneyUtil

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
        sql, params, table_name = self.toSelectSQL(entity)

        sql = SqlUtil.add_paging(sql, start, size)
        return sql, params, table_name

    def toUpdateSQL(self, entity):
        fieldAndValue = self.__getKeyValue(entity)
        pk = HoneyUtil.get_pk(entity)
        if not pk:
            if SysConst.id in fieldAndValue:
                pk = SysConst.id
            else:
                raise SqlBeeException("update by id, bean should has id field or need set the pk field name with __pk__")

        pkvalue = fieldAndValue.pop(pk, None)
        if not pkvalue:
            raise SqlBeeException("the id/pk value can not be None")

        conditions = {pk:pkvalue}

        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_update_sql(table_name, fieldAndValue, conditions)

    def toUpdateBySQL2(self, entity, condition, whereFields):
        fieldAndValue, classField = self.__getKeyValue_classField(entity)
        ext = list(set(whereFields) - set(classField))
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

        cls = type(entity_list[0])
        classField = HoneyUtil.get_class_field(cls)
        sql = self.__build_insert_batch_sql(table_name, classField)
        list_params = HoneyUtil.get_list_params(classField, entity_list)

        return sql, list_params, table_name

    def toSelectByIdSQL(self, entity_class, length):
        classField = HoneyUtil.get_class_field(entity_class)  # list
        where_condition_str = self._toWhereById(entity_class, length)

        table_name = HoneyUtil.get_table_name_by_class(entity_class)

        return self.__build_select_by_id_sql(table_name, classField, where_condition_str), table_name

    def _toWhereById(self, entity_class, length):

        pk = HoneyUtil.get_pk_by_class(entity_class)
        if not pk:
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
        return self.__build_delete_by_id_sql(table_name, where_condition_str), table_name

    # def _toById(self, entity):
    #     fieldAndValue, classField = self.__getKeyValue_classField(entity)
    #     pk = HoneyUtil.get_pk(entity)
    #     if pk is None:
    #         if SysConst.id in fieldAndValue:
    #             pk = SysConst.id
    #         else:
    #             raise SqlBeeException("by id, bean should has id field or need set the pk field name with __pk__")
    #
    #     pkvalue = fieldAndValue.pop(pk, None)
    #     if pkvalue is None:
    #         raise SqlBeeException("the id/pk value can not be None")
    #
    #     conditions = {pk:pkvalue}
    #     return classField, conditions

    def toSelectFunSQL(self, entity, functionType, field_for_fun):
        fieldAndValue, _ = self.__getKeyValue_classField(entity)

        table_name = HoneyUtil.get_table_name(entity)
        return self.__build_select_fun_sql(table_name, functionType, field_for_fun, fieldAndValue)

    def __getKeyValue(self, entity):
        fieldAndValue, _ = self.__getKeyValue_classField(entity)
        return fieldAndValue

    # __  or _只是用于范围保护，转成sql时，将这两种前缀统一去掉
    def __getKeyValue_classField(self, entity):
        return ParseSqlHelper._getKeyValue_classField(entity)

        # cls = type(entity)
        # # already use cache
        # classField = HoneyUtil.get_class_field(cls)  # list
        # fieldAndValue = HoneyUtil.get_obj_field_value(entity)  # dict
        #
        # classFieldAndValue = HoneyUtil.get_class_field_value(cls)
        #
        # fieldAndValue = HoneyUtil.remove_prefix(fieldAndValue)
        #
        # objKey = fieldAndValue.keys()
        #
        # set1 = set(classField)
        # set2 = set(objKey)  # list转set 顺序会乱了
        # setExt = set2 - set1
        #
        # # 默认删除动态加的属性
        # for k in setExt:
        #     fieldAndValue.pop(k, None)
        #
        # # 若对象的属性的值是None，则使用类级别的
        # for name, value in fieldAndValue.items():
        #     if value is None:
        #         fieldAndValue[name] = classFieldAndValue[name]
        #
        # # 当对象的属性没有相应的值，而类的属性有，则使用类级的属性
        # for name, value in classFieldAndValue.items():
        #     if value is not None and fieldAndValue.get(name, None) is None:
        #         fieldAndValue[name] = value
        #
        # # 排除value为None的项
        # fieldAndValue = {key: value for key, value in fieldAndValue.items() if value is not None}
        #
        # return  fieldAndValue, classField

    def __getPlaceholder(self):
        return ParseSqlHelper._getPlaceholder()

    # updateById
    def __build_update_sql(self, table_name, set_dict, entityFilter):
        # entityFilter just pk
        if not set_dict:
            raise SqlBeeException("Update SQL's set part is empty!")

        # if not entityFilter:  #还没有用到
        #     Logger.warn("Update SQL's where part is empty, would update all records!")

        set_dict2 = self.__toColumns_with_dict(set_dict)
        conditions2 = self.__toColumns_with_dict(entityFilter)

        ph = self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            updateSet = ', '.join(f"{key} = {ph}{key}" for key in set_dict2.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in conditions2.keys())
        else:
            updateSet = ', '.join(f"{key} = {ph}" for key in set_dict2.keys())
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in conditions2.keys())

        # sql = f"UPDATE {table_name} SET {updateSet} WHERE {condition_str}"
        sql = f"{K.update()} {table_name} {K.set()} {updateSet} {K.where()} {condition_str}"
        params = list(set_dict2.values()) + list(conditions2.values())
        return sql, params, table_name

    def __build_insert_sql(self, table_name, data):
        if not data:
            raise SqlBeeException("insert column and value is empty!")

        data2 = self.__toColumns_with_dict(data)

        ph = self.__getPlaceholder()
        columns = ', '.join(data2.keys())
        if self.__getPlaceholderType() == 3:
            placeholders = ', '.join(f" {ph}{key}" for key in data2.keys())
        else:
            placeholders = ', '.join(f"{ph}" for _ in data2)
        sql = f"{K.insert()} {K.into()} {table_name} ({columns}) {K.values()} ({placeholders})"
        return sql, list(data2.values()), table_name

    def __build_insert_batch_sql(self, table_name, classField):
        if not classField:
            raise SqlBeeException("column list is empty!")

        columns = self.__toColumns(classField)

        ph = self.__getPlaceholder()
        columnsStr = ', '.join(columns)
        if self.__getPlaceholderType() == 3:
            placeholders = ', '.join(f" {ph}{item}" for item in classField)
        else:
            placeholders = ', '.join(f"{ph}" for _ in classField)
        sql = f"{K.insert()} {K.into()} {table_name} ({columnsStr}) {K.values()} ({placeholders})"
        return sql

    def __toColumns_with_dict(self, kv):
        # if not kv:
        #     return None
        # return {NamingHandler.toColumnName(k):v for k, v in kv.items()}
        return ParseSqlHelper._toColumns_with_dict(kv)

    def _build_where_filter(self, entityFilter):
        return ParseSqlHelper._build_where_filter(entityFilter)

        # entityFilter2 = self.__toColumns_with_dict(entityFilter)
        #
        # ph = self.__getPlaceholder()
        # if self.__getPlaceholderType() == 3:
        #     condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in entityFilter2.keys())
        # else:
        #     condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in entityFilter2.keys())
        # return condition_str

    def __toColumns(self, classField):
        return [NamingHandler.toColumnName(field) for field in classField]

    def __build_select_sql(self, table_name, classField, entityFilter = None):
        if not classField:
            raise SqlBeeException("column list is empty!")

        columns = self.__toColumns(classField)
        # sql = f"SELECT * FROM {table_name}"
        # sql = f"SELECT {', '.join(classField)} FROM {table_name}"
        sql = f"{K.select()} {', '.join(columns)} {K.from_()} {table_name}"

        # where part
        params = []
        if entityFilter:
            condition_str = self._build_where_filter(entityFilter)
            sql += f" {K.where()} {condition_str}"
            params = list(entityFilter.values())
        return sql, params, table_name

    def __build_select_sql2(self, table_name, classField, entityFilter = None, condition = None):

        conditionStruct = None
        selectFields = None

        if condition:
            conditionStruct = condition.parseCondition()
            selectFields = conditionStruct.selectFields

        if not selectFields and not classField:
            raise SqlBeeException("column list is empty!")

        if selectFields:
            columns = self.__toColumns(selectFields)
        else:
            columns = self.__toColumns(classField)

        sql = f"{K.select()} {', '.join(columns)} {K.from_()} {table_name}"

        # where part
        params = []
        if entityFilter:
            condition_str = self._build_where_filter(entityFilter)
            sql += f" {K.where()} {condition_str}"
            params = list(entityFilter.values())

        if conditionStruct:
            sql, params = self.__appendWhere(sql, params, entityFilter, conditionStruct)
            start = conditionStruct.start
            size = conditionStruct.size
            if start or start == 0 or size:
                sql = SqlUtil.add_paging(sql, start, size)
            if conditionStruct.has_for_update:
                sql += " " + K.for_update()

        return sql, params, table_name

    def __appendWhere(self, sql, params, entityFilter, conditionStruct):
        return ParseSqlHelper._appendWhere(sql, params, entityFilter, conditionStruct)

        # if conditionStruct:
        #     condition_where = conditionStruct.where
        #     if condition_where:
        #         values = conditionStruct.values
        #         if entityFilter:
        #             sql += " " + K.and_()
        #         else:
        #             sql += " " + K.where()
        #         sql += " " + condition_where
        #         params = params + values
        # return sql, params

    def __build_delete_sql2(self, table_name, entityFilter, condition = None):
        sql = f"{K.delete()} {K.from_()} {table_name}"
        params = []
        if entityFilter:
            condition_str = self._build_where_filter(entityFilter)
            sql += f" {K.where()} {condition_str}"
            params = list(entityFilter.values())

        if condition:
            condition.suidType(SuidType.DELETE)
            conditionStruct = condition.parseCondition()
            sql, params = self.__appendWhere(sql, params, entityFilter, conditionStruct)

        return sql, params, table_name

    def __build_update_by_sql2(self, table_name, entityFilter, condition, whereFields):

        # 处理来自实体的
        where_dict11 = {}
        set_dict11 = {}  # 是否有顺序，没有顺序，还要考虑是否符合要求 Python3.6后是有顺序的
        for key, value in entityFilter.items():
            if key in whereFields:
                where_dict11[key] = value
            else:
                set_dict11[key] = value

        null_value_filter = set(whereFields) - set(where_dict11)
        updateSetStr_inCondtion = None
        conditionUpdateSetStruct = None
        where = None

        if condition:
            condition.suidType(SuidType.UPDATE)
            conditionStruct = condition.parseCondition()
            where = conditionStruct.where
            # 还要检测是否在condition设置有，要是有，就不用使用is null
            null_value_filter = null_value_filter - conditionStruct.whereFields
            if not where_dict11 and not where and not null_value_filter:
                Logger.warn("Update SQL's where part is empty, would update all records!")

            conditionUpdateSetStruct = condition.parseConditionUpdateSet()
            updateSetStr_inCondtion = conditionUpdateSetStruct.updateSet

            if not set_dict11 and not updateSetStr_inCondtion:
                raise SqlBeeException("UpdateBy SQL's set part is empty!")
        else:
            if not set_dict11:
                raise SqlBeeException("UpdateBy SQL's set part is empty!")

        set_dict12 = self.__toColumns_with_dict(set_dict11)
        where12 = self.__toColumns_with_dict(where_dict11)  # 来自entityFilter

        condition_str = ""
        updateSet = None
        ph = self.__getPlaceholder()
        if self.__getPlaceholderType() == 3:
            if set_dict12:
                updateSet = ', '.join(f"{key} = {ph}{key}" for key in set_dict12.keys())
            if where12:
                condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in where12.keys())
        else:
            if set_dict12:
                updateSet = ', '.join(f"{key} = {ph}" for key in set_dict12.keys())
            if where12:
                condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in where12.keys())

        # 增加来自condition的update set部分
        if updateSetStr_inCondtion:
            if updateSet:
                updateSet += " , " + updateSetStr_inCondtion
            else:
                updateSet = updateSetStr_inCondtion

        if null_value_filter:  # null_value_filter transfer to where
            no_value_filter2 = self.__toColumns(null_value_filter)
            if condition_str:
                condition_str += " " + K.and_() + " "
            condition_str += f" {K.and_()} ".join(f"{key} {K.isnull()}" for key in no_value_filter2)

        if condition_str:
            sql = f"{K.update()} {table_name} {K.set()} {updateSet} {K.where()} {condition_str}"
        else:
            sql = f"{K.update()} {table_name} {K.set()} {updateSet}"

        params = []
        # 调整values:  entityFilter's set-> conditon's set-> entityFilter's where-> conditon's where
        if set_dict12:
            params = list(set_dict12.values())
        # 是否能够保证where12.keys()与where12.values()顺序对应.会保证
        # params = params+conditionUpdateSetStruct.values   + list(where12.values())
        if conditionUpdateSetStruct and conditionUpdateSetStruct.values:
            params += conditionUpdateSetStruct.values
        if where12:
            params += list(where12.values())

        if where:  # conditon's where
            sql, params = self.__appendWhere(sql, params, whereFields, conditionStruct)

        return sql, params, table_name

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

    def __get_dbname(self):
        return HoneyConfig().get_dbname()

    def __getPlaceholderType(self):
        return ParseSqlHelper._getPlaceholderType()

        # # sql = "SELECT * FROM employees WHERE employee_id = :emp_id"
        # # cursor.execute(sql, emp_id=emp_id)
        # # sql = "INSERT INTO employees (employee_id, employee_name, salary) VALUES (:emp_id, :emp_name, :emp_salary)"
        # # cursor.execute(sql, emp_id=emp_id, emp_name=emp_name, emp_salary=emp_salary)
        # if DatabaseConst.ORACLE.lower() == self.__get_dbname():
        #     return 3
        # else:
        #     return 0

    def __build_select_fun_sql(self, table_name, functionType, field_for_fun, conditions = None):
        column_for_fun = NamingHandler.toColumnName(field_for_fun)

        # sql = f"SELECT count() FROM {table_name}"
        sql = f"{K.select()} {functionType.get_name()}({column_for_fun}) {K.from_()} {table_name}"

        # where part
        params = []
        if conditions:
            condition_str = self._build_where_filter(conditions)
            sql += f" {K.where()} {condition_str}"
            params = list(conditions.values())
        return sql, params, table_name

    # ddl
    def toCreateSQL(self, cls):
        """根据实体类生成创建表的 SQL 语句"""

        NOT_NULL_STR = HoneyUtil.adjustUpperOrLower(" NOT NULL")
        UNIQUE_STR = HoneyUtil.adjustUpperOrLower(" UNIQUE")
        PK_STR = HoneyUtil.adjustUpperOrLower("PRIMARY KEY")
        CREATE_TABLE_STR = HoneyUtil.adjustUpperOrLower("CREATE TABLE")

        field_and_type = HoneyUtil.get_field_and_type(cls)

        # p1.主键
        pk = HoneyUtil.get_pk_by_class(cls)
        table_name = HoneyUtil.get_table_name_by_class(cls)
        if not pk:
            if SysConst.id in field_and_type:
                pk = SysConst.id
            else:
                Logger.warn("There are no primary key when create table: " + table_name)

        sql_fields = []
        addPkLast = None
        # p1.5 创建主键字段语句
        if pk:
            # pk_type = field_and_type.pop(pk, None)
            pk_type = field_and_type[pk]
            if pk_type and pk_type == str:
                field_and_type[pk] = None
            else:
                pk = NamingHandler.toColumnName(pk)
                temp_type = HoneyUtil.adjustUpperOrLower(HoneyUtil.generate_pk_statement())
                pk_statement = pk + temp_type
                # sql_fields.append(pk_statement)
                field_and_type.pop(pk, None)
                if " int(11)" == temp_type:
                    addPkLast = pk
                    pk_statement += NOT_NULL_STR

                sql_fields.append(pk_statement)

        unique_key_set = HoneyUtil.get_unique_key(cls)
        not_null_filels_set = HoneyUtil.get_not_null_filels(cls)

        for field_name, field_type in field_and_type.items():
            sql_type = HoneyUtil.python_type_to_sql_type(field_type)
            column_name = NamingHandler.toColumnName(field_name)
            temp_sql = f"{column_name} {sql_type}"
            if unique_key_set and field_name in unique_key_set:
                temp_sql += UNIQUE_STR
            if not_null_filels_set and field_name in not_null_filels_set:
                temp_sql += NOT_NULL_STR
            sql_fields.append(temp_sql)

        if addPkLast:
            sql_fields.append(f"{PK_STR}({addPkLast})")

        sql_statement = f"{CREATE_TABLE_STR} {table_name} (\n    " + ",\n    ".join(sql_fields) + "\n);"

        return sql_statement

    def toDropTableSQL(self, entityClass):
        # if type(entityClass) == str:
        if isinstance(entityClass, str):
            table_name = entityClass
        else:
            table_name = HoneyUtil.get_table_name_by_class(entityClass)
        dbname = HoneyConfig().get_dbname()
        if dbname == DatabaseConst.ORACLE.lower() or dbname == DatabaseConst.SQLSERVER.lower():
            sql0 = "DROP TABLE " + table_name
        else:
            sql0 = "DROP TABLE IF EXISTS " + table_name
        return sql0

    def to_index_sql(self, entity_class, fields, index_name, prefix, index_type_tip, index_type):
        if not fields:
            raise ValueError(f"Create {index_type_tip} index, the fields can not be empty!")

        NameCheckUtil.check_fields(fields)
        table_name = HoneyUtil.get_table_name_by_class(entity_class)
        # columns = self.transfer_field(fields, entity_class)
        columns = self.transfer_field(fields)

        if not index_name:
            index_name = f"{prefix}{table_name}_{columns.replace(',', '_')}"
        else:
            NameCheckUtil.check_fields(index_name)

        index_sql = f"CREATE {index_type}INDEX {index_name} ON {table_name} ({columns})"
        return index_sql

    # def transfer_field(self, fields, entity_class):
    def transfer_field(self, fields):
        return NamingHandler.toColumnName(fields)

    def to_drop_index_sql(self, entity_class, index_name):
        table_name = HoneyUtil.get_table_name_by_class(entity_class)
        dbname = HoneyConfig().get_dbname()

        if index_name:
            if dbname == DatabaseConst.SQLSERVER.lower():
                drop_sql = "DROP INDEX table_name.index_name"
            elif dbname == DatabaseConst.ORACLE.lower() or dbname == DatabaseConst.SQLite.lower() or dbname == DatabaseConst.DB2.lower():
                drop_sql = "DROP INDEX index_name"
            elif dbname == DatabaseConst.MYSQL.lower() or dbname == DatabaseConst.MsAccess.lower():
                drop_sql = "DROP INDEX index_name ON table_name"
            else:
                drop_sql = "DROP INDEX index_name"

            return drop_sql.replace("table_name", table_name).replace("index_name", index_name)
        else:
            return f"DROP INDEX ALL ON {table_name}"


class MoreObjToSQL:

    def __toColumns(self, classField):
        return [NamingHandler.toColumnName(field) for field in classField]
    
    def __addAliasForColumns(self, columnName, main_table):
        # 不是主表的字段，要加别名
        cols = []
        for f in columnName:
            fld = f.strip()
            prefix = main_table + '.'
            if fld.startswith(prefix):
                cols.append(fld)
                continue
            cols.append(f"{fld} '{fld}'")

        return cols 

    def __appendWhere(self, sql, params, entityFilter, conditionStruct):
        return ParseSqlHelper._appendWhere(sql, params, entityFilter, conditionStruct)

    def toSelectSQL(self, entity, condition: Condition = None):

        moreTableStructDict = ParseSqlHelper.get_joins_struct(entity)

        if moreTableStructDict is None or len(moreTableStructDict) == 0:
            raise SqlBeeException("Entity for Moretable operate must have JoinMeta setting!")

        # transform_result_for_moretable
        HoneyContext._set_data(LocalType.MoreTableStruct, type(entity), moreTableStructDict)

        fieldAndValue, classField = ParseSqlHelper._getKeyValue_classField_for_moretable(entity)
        table_name = HoneyUtil.get_table_name(entity)

        return self.__build_more_select_sql(table_name, classField, fieldAndValue, moreTableStructDict, condition)

    def __build_more_select_sql(self, table_name, classField, entityFilter, moreTableStructDict = None, condition = None):
        if not classField:
            raise SqlBeeException("column list is empty!")

        conditionStruct = None
        selectFields = None

        if condition:
            conditionStruct = condition.parseCondition()
            selectFields = conditionStruct.selectFields

        if not selectFields and not classField:
            raise SqlBeeException("column list is empty!")

        main_alias = table_name

        # 拿JoinMetea设置的main_alias
        i = 0
        moreTableStructOverall = None
        for mtStruct in moreTableStructDict.values():
            if i == 0 and mtStruct.main_alias:
                main_alias = mtStruct.main_alias
                moreTableStructOverall = mtStruct.overall
            i = i + 1
            break

        isDefineColumns = False
        if selectFields:
            columns = self.__toColumns(selectFields)
            columns = self.__addAliasForColumns(columns, main_alias)
            isDefineColumns = True
        else:
            columns = self.__toColumns(classField)

        need_rewrite_paging_sql = True
        # 0.用户主动设置本次查询不需要分页改写
        if condition and condition.isDoNotRewritePagingSql():
            need_rewrite_paging_sql = False
        elif conditionStruct:
                # 1. 有分组
                if conditionStruct.has_group:
                    need_rewrite_paging_sql = False
                # 2.有聚合查询; 不需要分页改写;

                # 3. 无分页
                # return (start != null && start > 1) || (size != null && size > 0);
                elif  not ((conditionStruct.start and conditionStruct.start > 1)  or  (conditionStruct.size and conditionStruct.size > 0)):
                    need_rewrite_paging_sql = False
                # 4.没有一对多
                elif moreTableStructOverall and not moreTableStructOverall.has_any_sublist_entity:
                    need_rewrite_paging_sql = False
        
            # TODO
            # 如果需要改写，则进一步优化;对于可以不改写也能准确分页的，则没必要改写，以提高查询效率。
            # 以下为伪代码，需转成具体实现
            # // 可以自动判断，决定是否进行准确分页改写；
            # // 需要改写分页sql，进行以下判断，看是否是真的需要改写
            # // 以下是必要非充分条件
            # // 1. 有分页
            # // 2. 有一对多
            #
            # // 以下有一条满足则不需要改写:
            # // 1.主表所有的主键设置有值或主表某个唯一约束列，可以确定最多只能查到一条主表记录；

        # process where filter
        if entityFilter:
            prefix = main_alias + "."
            entityFilter = {prefix + key: value for key, value in entityFilter.items()}

        if not isDefineColumns:
            prefixed_columns = [f"{main_alias}.{col}" for col in columns]
            full_columns = prefixed_columns
        else:
            full_columns = columns

        columns_set = set(columns)

        table_names = [table_name]

        sub_table_num = len(moreTableStructDict)
        join_clauses: List[str] = []
        where_join: List[str] = []
        where_join_table = ""

        for mtStruct in moreTableStructDict.values():
            sub_class = mtStruct.sub_class
            sub_table = HoneyUtil.get_table_name_by_class(sub_class)
            sub_alias = mtStruct.sub_alias

            sub_tablename = HoneyUtil.get_table_name_by_class(sub_class)
            table_names.append(sub_tablename)  # 用于缓存记录，要用真正的表名，不能用别名

            sub_object = mtStruct.sub_object

            # 加子表  子表名.字段 select列表
            if sub_object is None or not sub_object:
                subFieldAndValue, subClassField = ParseSqlHelper._getKeyValue_classField_ByClass_for_moretable(sub_class)
            else:
                subFieldAndValue, subClassField = ParseSqlHelper._getKeyValue_classField_for_moretable(sub_object)  # joins_struct要能获取子类的对象

            if subFieldAndValue:
                prefix = sub_alias + "."
                subFieldAndValue = {prefix + key: value for key, value in subFieldAndValue.items()}
                entityFilter.update(subFieldAndValue)

            sub_columns = self.__toColumns(subClassField)  # 考虑多表的字段

            if not isDefineColumns:
                #没有定义字段，则将字段放入full_columns
                for col in sub_columns:
                    if sub_table_num == 1 and col not in columns_set:
                        # full_columns.extend(pre_sub_columns)
                        full_columns.append(sub_alias + "." + col)
                    else:  # 超过1个子表,子表的列全部用别名
                        full_columns.append(f"{sub_alias}.{col} '{sub_alias}.{col}'")  # TODO 确认其它DB是否支持这种格式。别名带引号。

            join_type = mtStruct.joinType
            main_fields = mtStruct.main_fields
            sub_fields = mtStruct.sub_fields

            if mtStruct.has_next_layer and mtStruct.main_alias:
                first_alias = mtStruct.main_alias
            else:
                first_alias = main_alias

            # 组装 ON 条件：m.main_field = alias.sub_field
            on_parts: List[str] = []
            for mf, sf in zip(main_fields, sub_fields):
                on_parts.append(f"{first_alias}.{mf} = {sub_alias}.{sf}")

            if join_type == JoinType.WHERE:
                where_join_table += f", {sub_table} {sub_alias}"
                where_join.extend(on_parts)
            else:
                on_sql = f" {K.and_()} ".join(on_parts)
                clause = f"{join_type.get_name()} {sub_table} {sub_alias} {K.on()} {on_sql}"
                join_clauses.append(clause)
        joins_part = " ".join(join_clauses)

        sql = f"{K.select()} {', '.join(full_columns)} {K.from_()} {table_name} {main_alias}"

        tempTablePlaceholder = "#{temp-table-bee_paging}#"

        if need_rewrite_paging_sql:
            sql = sql + " " + tempTablePlaceholder

        sql2 = ""

        if where_join_table:
            sql2 += where_join_table

        where_join_sql = ""
        if where_join:
            where_join_sql = f" {K.and_()} ".join(where_join)

        # add join
        if joins_part:
            sql2 += f" {joins_part}"

        # where part
        had_where = False
        params = []
        if entityFilter:
            condition_str = ParseSqlHelper._build_where_filter(entityFilter)
            if where_join_sql:
                where_join_sql += f" {K.and_()} "
            sql2 += f" {K.where()} {where_join_sql}{condition_str}"
            had_where = True
            params = list(entityFilter.values())
        elif where_join:
            sql2 += f" {K.where()} {where_join_sql}"
            had_where = True

        if conditionStruct:
            sql2, params = self.__appendWhere(sql2, params, had_where, conditionStruct)

        sql = sql + sql2

        if need_rewrite_paging_sql:
            pagingRewriteSql = []
            pagingRewriteSql.append("select distinct ")
            pagingRewriteSql.append(table_name)
            pagingRewriteSql.append(".id")  # TODO 需要改为具体的主键；还要考虑多主键的情况   获取主键
            pagingRewriteSql.append(" from ")
            pagingRewriteSql.append(table_name)
            pagingRewriteSql.append(sql2)

            temp_sql = ''.join(pagingRewriteSql)

            params.extend(params)
            if conditionStruct:
                start = conditionStruct.start
                size = conditionStruct.size
                if start or start == 0 or size:
                    # paging
                    temp_sql = SqlUtil.add_paging(temp_sql, start, size)

            pagingRewriteSql = []  # reset pagingRewriteSql
            pagingRewriteSql.append("join (")
            pagingRewriteSql.append(temp_sql)
            pagingRewriteSql.append(") bee_paging on ")
            pagingRewriteSql.append(table_name)
            pagingRewriteSql.append(".id = bee_paging.id")  # TODO 需要改为具体的主键；还要考虑多主键的情况

            temp_paing_sql = ''.join(pagingRewriteSql)
            # print(temp_paing_sql)
            idx = sql.find(tempTablePlaceholder)
            if idx > -1:
                sql = sql[:idx] + temp_paing_sql + sql[idx + len(tempTablePlaceholder):]
        else:
            if conditionStruct:
                start = conditionStruct.start
                size = conditionStruct.size
                if start or start == 0 or size:
                    # paging
                    sql = SqlUtil.add_paging(sql, start, size)
                if conditionStruct.has_for_update:
                    sql += " " + K.for_update()

        return sql, params, table_names

