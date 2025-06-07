from enum import Enum, auto  

from bee.config import HoneyConfig

class FunctionType(Enum): 
    MAX = "max"  
    MIN = "min"  
    SUM = "sum"  
    AVG = "avg"  
    COUNT = "count"  

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

    def get_name(self): 
        return self.value  


class OrderType(Enum): 
    ASC = "asc"
    DESC = "desc"

    def get_name(self): 
        if HoneyConfig.sql_key_word_case == "upper": 
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
    # 数据类型标识枚举 
    CacheSuidStruct = auto()  # 对应原来的 sqlPreValueLocal  

    
