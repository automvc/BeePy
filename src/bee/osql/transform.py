from datetime import time
import json
from typing import Dict, List, Tuple, Set

from bee.context import HoneyContext
from bee.name.naming_handler import NamingHandler
from bee.osql.logger import Logger
from bee.util import HoneyUtil


class ResultUtil:
    
    """将结果集的一行转换为实体对象"""  

    @staticmethod
    def transform_result(row, column_names, entity_class): 
        
        field_and_type = HoneyUtil.get_field_and_type(entity_class)
        # 创建实体类的新实例
        obj = entity_class()
        for i in range(len(column_names)):
            fieldName = NamingHandler.toFieldName(column_names[i])
            # 获取字段的类型  
            field_type = field_and_type[fieldName]
            v = row[i]
            if field_type is bool:
                # v = bool(v)  # 将值转换为bool类型
                # print(type(v))
                if type(v) == int:
                    v = bool(v)
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
                v = row[i]
            setattr(obj, fieldName, v)
        return obj
    
    
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
            # return params
        
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

