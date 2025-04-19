
    
class CacheSuidStruct:
    sql:str  # 不带值的
    tableNames:str 
    params = None
    returnType:str  # 返回值类型用于过滤缓存的查询结果,防止同一查询sql的不同类型的结果;  但更改的操作可不需要用这个值
    suidType:str  # 操作类型
    entityClass = None
    
    def __init__(self, sql, params, tableNames, returnType, entityClass, suidType = None):
        self.sql = sql
        self.params = params
        self.tableNames = tableNames
        self.returnType = returnType
        self.entityClass = entityClass
        self.suidType = suidType
    
    def __str__(self):
        return str(self)
    

class TableMeta:
    col = None
    type = None
    ynNull:bool = None  # 是否允许为空
    ynKey:bool = None  # 是否是主键
    label = None  # 标题,列名注释
    defaultValue = None
    strLen:int = None
    unique:bool = None
    precision:int = None
    scale:int = None
    # tablecomment = None
    # tablename = None
    
    def __repr__(self): 
        return  str(self.__dict__) 