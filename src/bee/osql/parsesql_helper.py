from typing import Type, Dict

from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.exception import ConfigBeeException
from bee.name.naming_handler import NamingHandler
from bee.osql.const import DatabaseConst
from bee.osql.sqlkeyword import K
from bee.osql.struct import MoreTableStruct

from bee.anno import JoinTable
from bee.osql.util import HoneyUtil


class ParseSqlHelper:

    @staticmethod
    def _getKeyValue_classField(entity):

        cls = type(entity)
        return ParseSqlHelper.__getKeyValue_classField_ByClass(cls, entity)

    # __  or _只是用于范围保护，转成sql时，将这两种前缀统一去掉
    @staticmethod
    def _getKeyValue_classField_ByClass(entityClass):
        return ParseSqlHelper.__getKeyValue_classField_ByClass(entityClass, None)

    @staticmethod
    def _getKeyValue_classField_for_moretable(entity):

        cls = type(entity)
        # print(cls)
        if cls == list:
            # 子表是list类型时，只获取list中第一个元素的对象转为where条件。
            return ParseSqlHelper.__getKeyValue_classField_ByClass_for_moretable(type(entity[0]), entity[0])
        return ParseSqlHelper.__getKeyValue_classField_ByClass_for_moretable(cls, entity)

    # __  or _只是用于范围保护，转成sql时，将这两种前缀统一去掉
    @staticmethod
    def _getKeyValue_classField_ByClass_for_moretable(entityClass):
        return ParseSqlHelper.__getKeyValue_classField_ByClass_for_moretable(entityClass, None)

    @staticmethod
    def __getKeyValue_classField_ByClass_for_moretable(entityClass, entity):
        fieldAndValue, classField = ParseSqlHelper.__getKeyValue_classField_ByClass(entityClass, entity)

        joins = getattr(entityClass, "__joins__", None)
        if isinstance(joins, dict):
            # select子句不需要查子表名
            for k in joins.keys():
                if fieldAndValue:
                    fieldAndValue.pop(k, None)
                if classField and k in classField:
                    classField.remove(k)

        return fieldAndValue, classField

    # __  or _只是用于范围保护，转成sql时，将这两种前缀统一去掉
    @staticmethod
    def __getKeyValue_classField_ByClass(entityClass, entity):

        # entityClass = type(entity)
        # already use cache
        classField = HoneyUtil.get_class_field(entityClass)  # list
        if entity is None:
            fieldAndValue = None
            return  fieldAndValue, classField

        fieldAndValue = HoneyUtil.get_obj_field_value(entity)  # dict

        classFieldAndValue = HoneyUtil.get_class_field_value(entityClass)

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

        # 排除value为None的项
        fieldAndValue = {key: value for key, value in fieldAndValue.items() if value is not None}

        return  fieldAndValue, classField

    # __joins_struct_cache = {}

    @staticmethod
    def get_joins_struct(entity: Type) -> Dict[str, MoreTableStruct]:
        return ParseSqlHelper.parse_joins(entity)

        # 不能用缓存，不同的对象有不同的值，对应不同的sql
        # clazz = type(entity)
        # joins_struct = HoneyUtil.__joins_struct_cache.get(clazz, None)
        # if joins_struct is None:
        #     joins_struct = HoneyUtil.parse_joins(entity)
        #     HoneyUtil.__joins_struct_cache[clazz] = joins_struct
        # return joins_struct

    @staticmethod
    def parse_joins(entity) -> Dict[str, MoreTableStruct]:
        # entity是对象，类型都可以
        """
        解析给定模型类中的 __joins__，返回结构化信息列表。
        每个元素包含：
        {fieldname/sub_alias:MoreTableStruct}
        """
        result: Dict[str, MoreTableStruct] = {}
        if entity is None:
            return result

        joins = getattr(entity, "__joins__", None)
        if not isinstance(joins, dict):
            return result

        for fieldname, meta in joins.items():
            if isinstance(meta, JoinTable):
                layer = 2
                ptree = []
                type_tree = [HoneyUtil.get_type(entity)]
                moreTableStruct = MoreTableStruct(meta, fieldname, entity, layer, ptree)

                # result[fieldname] = moreTableStruct
                result[moreTableStruct.sub_alias] = moreTableStruct
                ptree.append(moreTableStruct.sub_alias)  # sub_alias是new之后才计算得到
                type_tree.append(HoneyUtil.get_type(moreTableStruct.sub_class))
                moreTableStruct.type_tree = type_tree
                # print(type_tree)

                
                sub_type = ", class is: ";
                if moreTableStruct.current_is_list:
                    sub_type = ", class is List, element type is:";

                print(f"The layer is: {layer}{sub_type} {HoneyUtil.get_type(moreTableStruct.sub_class)}, alias is: {moreTableStruct.sub_alias}")
                
                old_size = len(result)
                print(moreTableStruct.has_next_layer)
                # check One has One
                ParseSqlHelper._parse_one_has_one(moreTableStruct, result, layer, ptree)
                new_size = len(result)
                if new_size > old_size:
                    moreTableStruct.has_next_layer = True  # set for layer 2
                print(moreTableStruct.has_next_layer)

                # #check One has One
                # sub_object_or_class=moreTableStruct.sub_object
                # if sub_object_or_class is None:
                #     sub_object_or_class=moreTableStruct.sub_class()
                # joins2 = getattr(sub_object_or_class, "__joins__", None)
                # # print(joins2)
                # if joins2:
                #     for fieldname2, meta2 in joins2.items():
                #         if isinstance(meta2, JoinTable):
                #             moreTableStruct2 = MoreTableStruct(meta2, fieldname2, sub_object_or_class, True, moreTableStruct.sub_alias)
                #             result[moreTableStruct2.sub_alias] = moreTableStruct2
                #         else:
                #             sub_class = HoneyUtil.get_type(sub_object_or_class)
                #             raise ConfigBeeException(f"have error join struct in {sub_class}, need use JoinTable")
            else:
                # clazz = type(entity)
                clazz = HoneyUtil.get_type(entity)
                raise ConfigBeeException(f"have error join struct in {clazz}, need use JoinTable")

        return result

    @staticmethod
    def _parse_one_has_one(current_moreTableStruct, result: Dict[str, MoreTableStruct], layer, ptree):
        # check One has One
        sub_object_or_class = current_moreTableStruct.sub_object
        if sub_object_or_class is None:
            sub_object_or_class = current_moreTableStruct.sub_class()
        joins2 = getattr(sub_object_or_class, "__joins__", None)

        if joins2:
            layer = layer + 1

            if layer >= 10:
                print(f"MoreTable do not support the join layer more than {layer}! It will be ignored!")
                return

            for fieldname2, meta2 in joins2.items():
                if isinstance(meta2, JoinTable):
                    current_type = HoneyUtil.get_type(meta2.sub_class)
                    if current_type in current_moreTableStruct.type_tree:
                        continue

                    current_ptree = ptree.copy()
                    # current_ptree = list(ptree)
                    moreTableStruct2 = MoreTableStruct(meta2, fieldname2, sub_object_or_class, layer, current_ptree, True, current_moreTableStruct.sub_alias)

                    if moreTableStruct2.sub_alias in result:
                        # 还要检测 自我查询的情况，是否可以。 todo
                        print(f"{moreTableStruct2.sub_alias} already exist, will change it to {moreTableStruct2.sub_alias}_1")
                        moreTableStruct2.sub_alias = moreTableStruct2.sub_alias + "_1"

                    current_type_tree = list(current_moreTableStruct.type_tree)
                    current_type_tree.append(HoneyUtil.get_type(moreTableStruct2.sub_class))
                    moreTableStruct2.type_tree = current_type_tree
                    result[moreTableStruct2.sub_alias] = moreTableStruct2
                    # print(current_type_tree)

                    current_ptree.append(moreTableStruct2.sub_alias)
                    sub_type = ", class is: ";
                    if moreTableStruct2.current_is_list:
                        sub_type = ", class is List, element type is:";
                    print(f"The layer is: {layer}{sub_type} {HoneyUtil.get_type(moreTableStruct2.sub_class)}, alias is: {moreTableStruct2.sub_alias}")
                    
                    ParseSqlHelper._parse_one_has_one(moreTableStruct2, result, layer, current_ptree)
                else:
                    sub_class = HoneyUtil.get_type(sub_object_or_class)
                    raise ConfigBeeException(f"have error join struct in {sub_class}, need use JoinTable")

    @staticmethod
    def _getPlaceholder():
        return HoneyContext.get_placeholder()  # TODO

    @staticmethod
    def _getPlaceholderType():
        # sql = "SELECT * FROM employees WHERE employee_id = :emp_id"
        # cursor.execute(sql, emp_id=emp_id)
        # sql = "INSERT INTO employees (employee_id, employee_name, salary) VALUES (:emp_id, :emp_name, :emp_salary)"
        # cursor.execute(sql, emp_id=emp_id, emp_name=emp_name, emp_salary=emp_salary)
        if DatabaseConst.ORACLE.lower() == HoneyConfig().get_dbname():
            return 3
        else:
            return 0

    @staticmethod
    def _toColumns_with_dict(kv):
        if not kv:
            return None
        return {NamingHandler.toColumnName(k):v for k, v in kv.items()}

    @staticmethod
    def _build_where_filter(entityFilter):
        entityFilter2 = ParseSqlHelper._toColumns_with_dict(entityFilter)

        ph = ParseSqlHelper._getPlaceholder()
        if ParseSqlHelper._getPlaceholderType() == 3:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}{key}" for key in entityFilter2.keys())
        else:
            condition_str = f" {K.and_()} ".join(f"{key} = {ph}" for key in entityFilter2.keys())
        return condition_str

    @staticmethod
    def _appendWhere(sql, params, entityFilter, conditionStruct):
        if conditionStruct:
            condition_where = conditionStruct.where
            if condition_where:
                values = conditionStruct.values
                if entityFilter:
                    sql += " " + K.and_()
                else:
                    sql += " " + K.where()
                sql += " " + condition_where
                params = params + values
        return sql, params

