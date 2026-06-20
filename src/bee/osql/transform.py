from datetime import time
import json
from typing import Dict, List, Tuple, Set

from bee.context import HoneyContext
from bee.name.naming_handler import NamingHandler
from bee.osql.logger import Logger

from bee.osql.util import HoneyUtil


class ResultUtil:

    @staticmethod
    def transform_result(row, column_names, entity_class):
        """将结果集的一行转换为实体对象"""

        field_and_type = HoneyUtil.get_field_and_type(entity_class)
        # 创建实体类的新实例
        obj = entity_class()
        for i in range(len(column_names)):
            fieldName = NamingHandler.toFieldName(column_names[i])
            if fieldName not in field_and_type:
                continue
            # 获取字段的类型
            field_type = field_and_type[fieldName]
            v = ResultUtil._transform_value(field_type, row[i])
            setattr(obj, fieldName, v)
        return obj

    @staticmethod
    def transform_result3(row, column_names, entity_class, moreTableStructDict):
        # transform_result_for_moretable3
        """将结果集的一行转换为实体对象"""

        subObject_cache_dict = {}
        sub_field_and_type_cache_dict = {}
        main_all_combination = []
        sub_field_value_str_cache_dict = {}

        field_and_type = HoneyUtil.get_field_and_type(entity_class)
        # 创建实体类的新实例
        obj = entity_class()
        length = len(column_names)
        for i in range(length):
            # print(column_names[i])
            fieldName = NamingHandler.toFieldName(column_names[i])

            if fieldName not in field_and_type:
                # 没找到应该是子类的。 todo
                split_result = fieldName.split('.', 1)
                if len(split_result) == 1:  # 列不带表名
                    for struct in moreTableStructDict.values():
                        sub_alias = struct.sub_alias
                        sub_class = struct.sub_class
                        sub_field_and_type = HoneyUtil.get_field_and_type(sub_class)
                        if split_result[0] in sub_field_and_type:
                            tab = sub_alias
                            sub_fieldName = split_result[0]
                            sub_field_and_type_cache_dict[tab] = sub_field_and_type
                            break
                else:  # 带表名, eg: tablename.name
                    # 分别获取两段内容
                    tab = split_result[0]
                    sub_fieldName = split_result[1]

                subObject = subObject_cache_dict.get(tab, None)
                sub_field_combination = sub_field_value_str_cache_dict.get(tab, None)
                sub_field_and_type = sub_field_and_type_cache_dict.get(tab, None)
                if subObject is None:
                    struct = moreTableStructDict[tab]
                    subClass = struct.sub_class
                    subObject = subClass()
                    subObject_cache_dict[tab] = subObject
                    sub_field_combination = []
                    sub_field_value_str_cache_dict[tab] = sub_field_combination
                    sub_field_and_type = HoneyUtil.get_field_and_type(subClass)
                    sub_field_and_type_cache_dict[tab] = sub_field_and_type

                sub_field_type = sub_field_and_type[sub_fieldName]
                v = ResultUtil._transform_value(sub_field_type, row[i])
                setattr(subObject, sub_fieldName, v)
                sub_field_combination.append(str(v))
            else:  # 主表的字段
                # 获取字段的类型
                field_type = field_and_type[fieldName]
                v = ResultUtil._transform_value(field_type, row[i])
                main_all_combination.append(str(v))
                setattr(obj, fieldName, v)
        # main_all_combination.extend(sub_field_value_str_cache_dict.get('student'))
        return obj, "#".join(main_all_combination), sub_field_value_str_cache_dict, subObject_cache_dict

    @staticmethod
    def _transform_value(field_type, v):
        original = v
        if field_type is bool:
            if v is None:
                pass
            # if type(v) == int:
            elif isinstance(v, int):
                v = bool(v)
            elif isinstance(v, bytes):
                v = (v == b'\x01')
            else:
                v = (v == '1') or (v.lower() == 'true')
        elif field_type in (dict, list, Dict, List):
            # v=dict(row[i])
            if v:
                try:
                    v = json.loads(v)
                except Exception as e:
                    Logger.warn("transform '" + v + "' to json have exception! " + str(e))
        elif field_type in (tuple, Tuple):
            if v:
                try:
                    v = tuple(json.loads(v))
                except Exception as e:
                    Logger.warn("transform '" + v + "' to json have exception! " + str(e))
        elif field_type in (set, Set):
            # set不保证顺序和原来的一样
            if v:
                try:
                    v = set(json.loads(v))
                except Exception as e:
                    Logger.warn("transform '" + v + "' to json have exception! " + str(e))
        else:
            v = original

        return v


class ParamUtil:

    @staticmethod
    def transform_param(params: list):

        if not params:
            return params

        new_params = []
        for item in params:
            # 这里不需要判断Dict,List等，因value会是实现的类型，List只是类型提示。
            if isinstance(item, dict) or isinstance(item, list) or isinstance(item, tuple):
                # new_params.append(str(item))
                new_params.append(json.dumps(item))
            elif isinstance(item, set):
                new_params.append(json.dumps(list(item)))
            elif HoneyContext.isSQLite() and isinstance(item, time):
                new_params.append(item.strftime('%H:%M:%S'))
            else:
                new_params.append(item)
        return new_params

    @staticmethod
    def transform_list_tuple_param(params):
        if not params:
            return params

        converted_params = []
        for item in params:
            # 将 tuple 转换为 list，调用 transform_param 方法
            transformed_list = ParamUtil.transform_param(list(item))
            # 将处理后的 list 转换回 tuple
            converted_params.append(tuple(transformed_list))
        return converted_params

