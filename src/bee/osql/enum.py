from enum import Enum  

from bee.config import PreConfig


# class EnumCaseMeta(EnumMeta):  
#     def __getattribute__(self, name):  
#         value = super().__getattribute__(name)  
#         if isinstance(value, self._enum_type_):  
#             enum_member = value  
#             if PreConfig.sql_key_word_case == "upper":  
#                 return enum_member._name_  
#             else:  
#                 return enum_member._name_.lower()  
#         return value  
    
# class FunctionType(Enum, metaclass=EnumCaseMeta): 
class FunctionType(Enum): 
    MAX = "max"  
    MIN = "min"  
    SUM = "sum"  
    AVG = "avg"  
    COUNT = "count"  

    # def get_name(self): 
    #     return self.value
    def get_name(self): 
        if PreConfig.sql_key_word_case == "upper":  
            return self.value.upper()  
        else:  
            return self.value.lower()  


class SuidType(Enum): 
    SELECT = "SELECT"  
    UPDATE = "UPDATE"  
    INSERT = "INSERT"  
    DELETE = "DELETE"  
    MODIFY = "MODIFY"  
    SUID = "SUID"  
    DDL = "DDL"  

    def __init__(self, type_string): 
        self.type = type_string  

    # def getType(self):  # 为了更贴近 Java 的 getter 方法命名  
    #     return self.type  

    # @property  #  或者使用 property 装饰器  
    def get_name(self): 
        return self.value  


class OrderType(Enum): 
    ASC = "asc"
    DESC = "desc"

    # def get_name(self): 
    #     return self.value  
    def get_name(self):  
        if PreConfig.sql_key_word_case == "upper":  
            return self.value.upper()  
        else:  
            return self.value.lower()  

    def __str__(self): 
        return self.get_name() 

class Op(Enum): 
    eq = "="  
    gt = ">"  
    lt = "<"  
    ne = "!="  
    ge = ">="  
    le = "<="  
    like = " like "  
    like_left = " like "  
    like_right = " like "  
    like_left_right = " like "
    # not_like = " not like "  
    in_ = " in"  
    not_in = " not in"  
    # is_null = "IS NULL"  
    # is_not_null = "IS NOT NULL"  

    def get_name(self): 
        return self.value  

    def __str__(self): 
        return self.get_name() 
    
