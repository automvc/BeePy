from bee.api import PreparedSql
from bee.context import HoneyContext
from bee.gen import TableMeta
from bee.name.naming_handler import NamingHandler
from bee.osql.obj2sql import ObjToSQL
from bee.util import HoneyUtil

from bee.osql.mid_typing import *


class Model: 
    __subclasses__ = []  
    
    def __init_subclass__(self, **kwargs): 
        if "<class 'bee.osql.mid.MidSQL.Model'>" != str(self):
            super().__init_subclass__(**kwargs) 
            Model.__subclasses__.append(self)  
            self.__table__ = type('Table', (), {'columns': []})  
    
    def __init__(self): 
        # 收集所有Column属性  
        for name, value in self.__class__.__dict__.items(): 
            if isinstance(value, Column): 
                value.name = name  
                self.__table__.columns.append(value)  


class MidSQL: 
     
    class Model(Model): 
        pass  
    
    # 添加类型属性  
    Integer = Integer() 
    SmallInteger = SmallInteger()
    SMALLINT = SMALLINT() 
    BigInteger = BigInteger()
    Boolean = Boolean()
    
    @property
    def String(self): 
        return String  
    
    @property
    def Numeric(self): 
        return Numeric
    
    @property
    def DECIMAL(self): 
        return DECIMAL
    
    Text = Text()
    
    JSON = JSON()
    
    DateTime = DateTime()
    Date = Date()
    Time = Time()
    
    REAL = REAL()
    Float = Float()
    
    def Column(self, *args, **kwargs): 
        return Column(*args, **kwargs) 
    
    def __default_type(self):
        try:
            if HoneyContext.isOracle():
                return "VARCHAR2"
            else:
                return "VARCHAR"
        except Exception: 
            return "VARCHAR"
    
    def to_create_all_sql(self, entity = None): 
        
        NOT_NULL_STR = HoneyUtil.adjustUpperOrLower(" NOT NULL")
        # NULL_STR = HoneyUtil.adjustUpperOrLower(" NULL")
        UNIQUE_STR = HoneyUtil.adjustUpperOrLower(" UNIQUE")
        PK_STR = HoneyUtil.adjustUpperOrLower("PRIMARY KEY")
        CREATE_TABLE_STR = HoneyUtil.adjustUpperOrLower("CREATE TABLE")
        
        all_sql = []
        table_names = []
        
        for model in Model.__subclasses__: 
            if not (entity is None or entity == model): 
                continue
            # print(model)
            # 实例化模型以收集列信息
            model_instance = model()
            
            # unique_list = []
            meta_list = []  # 存储所有TableMeta对象的列表
            addPkLast = None
            for column in model_instance.__table__.columns: 
                # 创建TableMeta对象并填充属性  
                meta = TableMeta()  
                meta.col = column.name  
                meta.type = str(column.type)  
                meta.ynNull = column.nullable  
                meta.ynKey = column.primary_key  
                meta.unique = column.unique
                
                # if column.unique:
                #     unique_list.append(column.unique)  
                
                # 特殊处理String类型的长度
                if isinstance(column.type, String): 
                    meta.strLen = column.type.length  
                    
                if isinstance(column.type, Numeric): 
                    meta.precision = column.type.precision 
                    meta.scale = column.type.scale 
                
                meta_list.append(meta)
                
            sql_fields = []
            sql_statement = ""          
            for meta in meta_list:
                column = NamingHandler.toColumnName(meta.col) 
                col_type = HoneyUtil.adjustUpperOrLower(meta.type)
                
                temp_sql = ""
                
                if meta.ynKey:
                    temp_type = HoneyUtil.generate_pk_statement()
                    temp_sql = column + temp_type
                    if " int(11)" == temp_type:
                        addPkLast = column
                        temp_sql += NOT_NULL_STR
                    temp_sql = HoneyUtil.adjustUpperOrLower(temp_sql)
                elif meta.type == 'String':
                    # col_type = HoneyUtil.adjustUpperOrLower(self.__default_type())
                    col_type = HoneyUtil.adjustUpperOrLower(HoneyUtil.mid_type_to_sql_type(meta.type))
                    if not meta.strLen:
                        meta.strLen=255
                    col_type += '(' + str(meta.strLen) + ')'
                    temp_sql = f"{column} {col_type}"
                elif meta.type == 'Text':
                    
                    if meta.strLen:
                        col_type += '(' + meta.strLen + ')'
                    temp_sql = f"{column} {col_type}"
                else:
                    col_type = HoneyUtil.adjustUpperOrLower(HoneyUtil.mid_type_to_sql_type(meta.type))
                    temp_sql = f"{column} {col_type}"
                    if meta.type == 'Numeric':
                        temp_sql += f"({meta.precision},{meta.scale})"
                    
                if meta.unique:
                    temp_sql += UNIQUE_STR  
                
                if not meta.ynKey: 
                    if meta.ynNull:
                        # temp_sql += NULL_STR
                        pass
                    else:
                        temp_sql += NOT_NULL_STR
                        
                sql_fields.append(temp_sql)
            
            if addPkLast:
                sql_fields.append(f"{PK_STR}({addPkLast})")
                
            sql_statement = f"{CREATE_TABLE_STR} {model.__name__} (\n    " + ",\n    ".join(sql_fields) + "\n);"  
            # print(sql_statement)
            all_sql.append(sql_statement)
            table_names.append(model.__name__)
        return all_sql, table_names
    
    def __create(self, is_drop_exist_table = None, entity_class = None):
    
        all_sql, table_names = self.to_create_all_sql(entity_class)
        pre = PreparedSql()
    
        if is_drop_exist_table:
            objToSQL = ObjToSQL()
            for tab_name in table_names:
                sql0 = objToSQL.toDropTableSQL(tab_name)
                pre.modify(sql0)
    
        for sql in all_sql:
            pre.modify(sql)
            
    def create_all(self, is_drop_exist_table = None):
        return self.__create(is_drop_exist_table = is_drop_exist_table)
            
    def create_one(self, entity_class, is_drop_exist_table = None):
        return self.__create(is_drop_exist_table = is_drop_exist_table, entity_class = entity_class)

