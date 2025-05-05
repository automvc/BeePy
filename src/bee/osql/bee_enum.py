from enum import Enum, auto  

from bee.config import HoneyConfig


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
        if HoneyConfig.sql_key_word_case == "upper": 
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

    # @property  #  或者使用 property 装饰器  
    def get_name(self): 
        return self.value  


class OrderType(Enum): 
    ASC = "asc"
    DESC = "desc"

    # def get_name(self): 
    #     return self.value  
    def get_name(self): 
        if HoneyConfig.sql_key_word_case == "upper": 
            return self.value.upper()  
        else: 
            return self.value.lower()  

    def __str__(self): 
        return self.get_name() 


class Op(Enum): 
    
    # def __new__(cls, value):  
    #     obj = object.__new__(cls)  
    #     obj._value_ = value  
    #     return obj
    
    # def __eq__(self, other):  
    #     if not isinstance(other, Op):  
    #         return NotImplemented  
    #     return self is other  # 强制使用身份比较  
    #
    # def __hash__(self):  
    #     return id(self)  # 确保每个成员哈希值不同 
    
    eq = "="  
    gt = ">"  
    lt = "<"  
    ne = "!="  
    ge = ">="
    le = "<="  
    
    
    # LIKE = "like"  
    # LIKE_LEFT = " like "
    # LIKE_RIGHT = " like "
    # LIKE_LEFT_RIGHT = " like "
    
    LIKE = ("like") 
    LIKE_LEFT = ("like", object())  # 添加唯一对象  
    LIKE_RIGHT = ("like", object())  # 添加唯一对象  
    LIKE_LEFT_RIGHT = ("like", object())  
    IN = "in"  
    NOT_IN = "not in"  
    
 

    def get_name(self): 
        # if type(self.value) in (tuple, list):
        if isinstance(self.value, (tuple, list)):
            return self.value[0]  # 返回原始字符串值  
        else:
            return self.value
        
    def __str__(self):
        return self.get_name() 

    # def __str__(self): 
    #     return self.value  
    
    
class LocalType(Enum): 
    """数据类型标识枚举"""  
    CacheSuidStruct = auto()  # 对应原来的 sqlPreValueLocal  
    # SQL_PRE_VALUE = auto()  # 对应原来的 sqlPreValueLocal  
    # SQL_INDEX = auto()  # 对应原来的 sqlIndexLocal  
    # CONDITION = auto()  # 对应原来的 conditionLocal  
    
