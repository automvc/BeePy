from enum import Enum  


class FunctionType(Enum): 
    MAX = "max"  
    MIN = "min"  
    SUM = "sum"  
    AVG = "avg"  
    COUNT = "count"  

    def get_name(self): 
        return self.value  


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

    @property  #  或者使用 property 装饰器  
    def type_value(self): 
        return self.type  
    
