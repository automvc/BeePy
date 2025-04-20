class Column: 

    def __init__(self, type_, primary_key = False, unique = False, nullable = True): 
        self.type = type_  
        self.primary_key = primary_key  
        self.unique = unique  
        self.nullable = nullable  
        self.name = None  # 会在Model的__init__中设置  


class Integer: 

    def __repr__(self): 
        return "Integer"

    
class SmallInteger: 

    def __repr__(self): 
        return "SmallInteger"


# class SmallInt:
#
#     def __repr__(self): 
#         return "SmallInt" 
    
    
class BigInteger:

    def __repr__(self): 
        return "BigInteger" 


class Boolean:

    def __repr__(self): 
        return "Boolean"


class String: 

    def __init__(self, length = None):
        self.length = length  
    
    def __repr__(self): 
        # return f"String({self.length})"  
        return f"String"  


class Text: 

    def __repr__(self): 
        return "Text"  

    
class JSON: 

    def __repr__(self): 
        return "JSON"  

    
class DateTime: 

    def __repr__(self): 
        return "DateTime"  

    
class Date: 

    def __repr__(self): 
        return "Date"  

    
class Time: 

    def __repr__(self): 
        return "Time"

    
class Float: 

    def __repr__(self): 
        return "Float"

class Numeric:  
    def __init__(self, precision, scale):  
        self.precision = precision  # 总位数（如10）  
        self.scale = scale          # 小数位数（如2）  
    
    def __repr__(self):  
        # return f"Numeric({self.precision}, {self.scale})"  
        return "Numeric"  

# 同 Numeric，别名
DECIMAL = Numeric

SMALLINT = SmallInteger

 
class REAL:

    def __repr__(self): 
        return "REAL"