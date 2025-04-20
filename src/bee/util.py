from bee.config import HoneyConfig
from bee.name.naming_handler import NamingHandler
from bee.osql.const import SysConst, DatabaseConst
from bee.osql.logger import Logger
from bee.osql.type_transform import Py2Sql, Sql2Py, Mid

from bee.custom import Custom
from bee.osql.mid_typing import Column


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
            prefix = "_" + class_name + "__"
            kv = { key[len(prefix):] if key.startswith(prefix) else key[1:] if key.startswith('_') else key: value
                   for key, value in cls.__dict__.items() if not (key.startswith('__') and key.endswith('__'))} 
            for key, value in kv.items():
                if isinstance(value, property):
                    kv[key] = None  # 使用get/set,暂时不能获取到bean的类级别的值。
                    # kv[key]=getattr(cls, key)
                elif isinstance(value, Column):
                    #print(value)
                    kv[key] = None
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
    
    """ 
    返回给定类的属性列表,但不包括系统的 
    since 1.6.0 还考虑字段的类型;时间类型等
    """ 

    @staticmethod
    def get_class_field(cls):
        fieldname_and_type_dict = HoneyUtil.get_field_and_type(cls)
        return fieldname_and_type_dict.keys()
    
    # 对象的不会改
    """ remove  __  or _ prefix """    
    @staticmethod
    def remove_prefix(dict_obj):
        if not dict_obj:
            return dict_obj
    
        fieldAndValue = {
            key[2:] if key.startswith('__') else key[1:] if key.startswith('_') else key: value  
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
        dict_n = {e: None for e in classField}
        # dict_classField=dict_n.copy()
        
        list_params = []
        for entity in entity_list: 
            obj_dict = HoneyUtil.get_obj_field_value(entity)
            dict_classField = dict_n.copy()
            for k, v in obj_dict.items():
                if v is not None and k in dict_classField:
                    dict_classField[k] = v
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
            else:
                if hasattr(cls, SysConst.id):
                    return SysConst.id
        return None  
    
    @staticmethod 
    def get_unique_key(cls): 
        return getattr(cls, SysConst.unique_key, None)     
    
    @staticmethod 
    def get_not_null_filels(cls): 
        return getattr(cls, SysConst.not_null_filels, None)   
    
    @staticmethod  
    def is_sql_key_word_upper(): 
        if HoneyConfig.sql_key_word_case:
            if HoneyConfig.sql_key_word_case == SysConst.upper:
                return True
        return False
    
    @staticmethod
    def generate_pk_statement(): 
        dbName = HoneyConfig().get_dbname()
        if dbName == DatabaseConst.MYSQL.lower(): 
            return " INT PRIMARY KEY AUTO_INCREMENT NOT NULL"  
        elif dbName == DatabaseConst.SQLite.lower(): 
            return " INTEGER PRIMARY KEY NOT NULL"  # 自动增长
        elif dbName == DatabaseConst.ORACLE.lower(): 
            return " NUMBER PRIMARY KEY"  
        elif dbName == DatabaseConst.PostgreSQL.lower(): 
            return " SERIAL PRIMARY KEY"  
        else: 
            # Logger.warn(f"Unsupported database type: {dbName}, when generate primary key!")
            Logger.warn(f"There is not dedicated primary key statement for: {dbName}, will use normal!")
            temp = " " + Custom.custom_pk_statement()
            # if column:
            #     temp += ",\n    PRIMARY KEY(" + column + ")"
            return temp
            # raise ValueError(f"Unsupported database type: {dbName}")  
    
    @staticmethod    
    def adjustUpperOrLower(value):
        
        isUpper = HoneyUtil.is_sql_key_word_upper()
        if isUpper:
            return value.upper()
        else:
            return value.lower()
  
    @staticmethod
    def python_type_to_sql_type(python_type): 
        type0 = Py2Sql().python_type_to_sql_type(python_type)
        return HoneyUtil.adjustUpperOrLower(type0)
    
    @staticmethod
    def sql_type_to_python_type(sql_type): 
        return Sql2Py().sql_type_to_python_type(sql_type)
    
    @staticmethod
    def mid_type_to_sql_type(mid_type): 
        mid = Mid()
        #直接找到，则直接返回
        sql_type = mid.mid_to_sqltype(mid_type)
        if sql_type:
            return sql_type
        
        python_type = mid.mid_to_python_type(mid_type)
        # print('aaa:',python_type)
        
        type0 = Py2Sql().python_type_to_sql_type(python_type)
        return HoneyUtil.adjustUpperOrLower(type0)
    
    @staticmethod
    def get_class_normal_field(cls):
        if hasattr(cls, '__dict__'): 
    # 过滤掉以__开头和结尾的键，并去掉前缀__和_   只是__开前开头，会变化的。
            class_name = cls.__name__
            prefix = "_" + class_name + "__"
            return [  
                key[len(prefix):] if key.startswith(prefix) else key[1:] if key.startswith('_') else key  
                for key in cls.__dict__.keys()   
                if not (key.startswith('__') and key.endswith('__'))  
            ]  
        else: 
            return None  
         
    __field_and_type_cache = {}  # V1.6.0 
    
    @staticmethod
    def get_field_and_type(cls): 
        field_and_type = HoneyUtil.__field_and_type_cache.get(cls, None)
        if field_and_type is None:
            field_and_type = HoneyUtil.__get_field_and_type(cls)
            HoneyUtil.__field_and_type_cache[cls] = field_and_type
        return field_and_type
    
    @staticmethod
    def __get_field_and_type(cls): 
        # 声明基本类型和无声明类型的字段（保留定义顺序）  
        A = HoneyUtil.get_class_normal_field(cls)
        
        B = {}
        try:
            # 保留有类型的;包括复合类型; 低版本没有使用时，会报异常
            # 3.8.10 have exception if no use like: remark: str = None
            B = cls.__annotations__
        except Exception:
            pass
        
        M = HoneyUtil.get_mid_field_and_type(cls)
        # print(M)
        if M:
            if not B:
                B = M
            else:
                B.update(M)
        
        # 保留有类型的;包括复合类型
        # B = cls.__annotations__  #3.8.10 have exception if no use like: remark: str = None
        new_map = {}
        
        # none_type_set=set(A)-set(B)
        # 复合类型  complex_type_set     
        ext = set(B) - set(A)
        
        if not ext:
            for f in A: 
                if f in B: 
                    # a1.声明类型的
                    new_map[f] = B[f]  
                else:
                    # a2.无类型声明
                    new_map[f] = None
        else:
            # A=A
            # B=B
            # ext=complex_type_set
            B_keys = list(B.keys())  
            
            # 使用简单的索引方式遍历 A 和 B  
            i, j = 0, 0  
            len_A, len_B = len(A), len(B_keys)  
            
            # 可以保证基本类型与无类型混合时的原始顺序
            while i < len_A and j < len_B:
                # b1.声明类型的
                if A[i] == B_keys[j]: 
                    new_map[B_keys[j]] = B[B_keys[j]]  
                    i += 1  
                    j += 1
                # b2.复合类型  
                elif B_keys[j] in ext: 
                    new_map[B_keys[j]] = B[B_keys[j]]
                    j += 1
                # b3.无类型声明 
                else: 
                    new_map[A[i]] = None  
                    i += 1
                    
            while i < len_A:
                new_map[A[i]] = None
                i += 1
                        
            while j < len_B:
                new_map[B_keys[j]] = B[B_keys[j]] 
                j += 1
                
            # 无声明类型与复合类型邻近，则无法识别；默认先处理复合类型(b2->b3)
            # descstr=None
            # modify_date: date
            # updated_at2: date
            # 结果变为：
            # modify_date DATE,
            # updated_at2 DATE,
            # descstr VARCHAR(255)
                
        return new_map
    
    @staticmethod
    def get_mid_field_and_type(cls):
        M = {}
        for name, obj in cls.__dict__.items(): 
            if isinstance(obj, Column):  # 确认是Column对象  
                field_type = obj.type  
                # print(f"字段名: {name}, 类型: {field_type}") 
                M[name] = Mid().mid_to_python_type(str(field_type))
        return M
                
