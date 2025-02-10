from enum import Enum  


class FunctionType(Enum): 
    MAX = "max"  
    MIN = "min"  
    SUM = "sum"  
    AVG = "avg"  
    COUNT = "count"  

    def get_name(self): 
        return self.value  
