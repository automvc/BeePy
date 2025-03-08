from bee.config import PreConfig
from bee.osql.const import SysConst

from bee.name.naming_handler import NamingHandler


# from bee.key import Key
class HoneyUtil: 
     
    """返回给定对象的属性字典，如果没有则返回None"""
    @staticmethod 
    def get_obj_field_value(obj): 
        if hasattr(obj, '__dict__'): 
            # print(obj.__dict__)
            return obj.__dict__  
        else: 
            return None 
        
    @staticmethod 
    def get_class_field_value(cls):
        
        if hasattr(cls, '__dict__'): 
            # 并去掉前缀__和_   只是__开前开头，会变化的。
            class_name = cls.__name__
            prefix="_"+class_name+"__"
            kv = { key[len(prefix):] if key.startswith(prefix) else key[1:] if key.startswith('_') else key: value
                   for key, value in cls.__dict__.items() if not (key.startswith('__') and key.endswith('__'))} 
            for key, value in kv.items():
                if isinstance(value, property):
                    kv[key]=None   #使用get/set,暂时不能获取到bean的类级别的值。
                    # kv[key]=getattr(cls, key)
            return kv
        else: 
            return None
        
        
        
        # if hasattr(cls, '__dict__'): 
        #     print(cls.__dict__)
        #     return {key: value for key, value in cls.__dict__.items() if (not (key.startswith('__') and key.endswith('__'))) and not isinstance(value, property)  } 
        # else: 
        #     return None
        
        # if hasattr(cls, '__dict__'):  
        #     return {  
        #         key: (getattr(cls, key)() if isinstance(getattr(cls, key), property) else getattr(cls, key))  
        #         for key in cls.__dict__.keys()  
        #         if not (key.startswith('__') and key.endswith('__'))  # 排除私有属性  
        #     }  
        # else:  
        #     return None  
        
        # result = {}  
        # for key in cls.__class__.__dict__:  
        #     # 排除私有属性  
        #     if not (key.startswith('__') and key.endswith('__')):  
        #         value = getattr(cls, key)  
        #         # 如果是property类型，则获取其值  
        #         if isinstance(value, property):  
        #             result[key] = getattr(cls, key)  # 通过实例获取属性值  
        #         else:  
        #             result[key] = value  
        # print(result)
        # return result  
    # dict: {'id': <property object at 0x000001E2C878D350>, 'name': <property object at 0x000001E2C878D3A0>, 'remark': <property object at 0x000001E2C878D3F0>}
    
    """ 返回给定类的属性列表,但不包括系统的 """ 
    @staticmethod
    def get_class_field(cls):
        if hasattr(cls, '__dict__'):  
    # 过滤掉以__开头和结尾的键，并去掉前缀__和_   只是__开前开头，会变化的。
            class_name = cls.__name__
            prefix="_"+class_name+"__"
            return [  
                key[len(prefix):] if key.startswith(prefix) else key[1:] if key.startswith('_') else key  
                for key in cls.__dict__.keys()   
                if not (key.startswith('__') and key.endswith('__'))  
            ]  
        else:  
            return None   
         
        # if hasattr(cls, '__dict__'):
        #     # 排除__开头且__结尾的 
        #     return [key for key in cls.__dict__.keys() if not (key.startswith('__') and key.endswith('__'))]  
        # else: 
        #     return None 
    
    # 对象的不会改
    """ remove  __  or _ prefix """    
    @staticmethod
    def remove_prefix(dict_obj):
        if dict_obj is None:
            return dict_obj
    
        fieldAndValue = {
            key[2:] if key.startswith('__') else key[1:] if key.startswith('_') else key: value  
            # key[1:] if key.startswith('_') else key: value 
            for key, value in dict_obj.items()
        }
        return fieldAndValue
    
    """获取对象的值元列表
    eg:
            # list_params = [
            #     (None, 'Alice', 30, 'Likes swimming', '123 Maple St'),
            #     (None, 'Charlie', 35, 'Enjoys hiking', None),
            #     (None, 'David', 28, None, None),  # remark 和 addr 均为空  
            #     ] 
    """
    @staticmethod
    def get_list_params(classField, entity_list):
        dict_n = {i:None for i in classField}
        # dict_classField=dict_n.copy()  //TODO
        
        list_params=[]
        for entity in entity_list:  
            obj_dict = HoneyUtil.get_obj_field_value(entity)
            dict_classField=dict_n.copy()
            for k, v in obj_dict.items():
                if v is not None and k in dict_classField:
                    dict_classField[k]=v
            list_params.append(tuple(dict_classField.values()))
        
        return list_params
    
    @staticmethod 
    def get_table_name(obj):
        cls = obj.__class__
        return HoneyUtil.get_table_name_by_class(cls)
        
    @staticmethod 
    def get_table_name_by_class(cls):
        # cls = obj.__class__
        temp_name = getattr(cls, '__tablename__', None)
        if temp_name and not temp_name.isspace():
            return temp_name
        class_name = cls.__name__  
        # table_name = class_name.lower()  # 还要应用多种转换规则 TODO
        # return table_name   
        return NamingHandler.toTableName(class_name)
    
    """ get pk from bean"""
    
    @staticmethod 
    def get_pk(obj):
        cls = obj.__class__
        return HoneyUtil.get_pk_by_class(cls)

    @staticmethod 
    def get_pk_by_class(cls):
        temp_name = getattr(cls, SysConst.pk, None)
        if temp_name and not temp_name.isspace():
            return temp_name
        else:
            temp_name = getattr(cls, SysConst.primary_key, None)
            if temp_name and not temp_name.isspace():
                return temp_name
        return None
            
    """将结果集的一行转换为实体对象"""        
    @staticmethod
    def transform_result(row, column_names, entity_class): 
        
        # 创建实体类的新实例
        obj = entity_class()
        for i in range(len(column_names)):
            setattr(obj, column_names[i], row[i])  # 像时间等类型，是否也可以自动设置？？？   TODO
        return obj
    
    @staticmethod  
    def is_sql_key_word_upper(): 
        # TODO support set in config file
        if PreConfig.sql_key_word_case:
            if PreConfig.sql_key_word_case == SysConst.upper:
                return True
        return False
            
