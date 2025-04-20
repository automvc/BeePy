from datetime import date, time, datetime 
import decimal
from typing import Dict, List, Set, Tuple

from bee.context import HoneyContext
from bee.osql.const import DatabaseConst
from bee.typing import String


class Py2Sql:
    __instance = None
    __import_check = True
    __ANNOTATED_SUPPORTED = False
    
    _type_mappings: Dict[str, Dict[str, str]] = {}
    
    def __new__(cls): 
        if cls.__instance is None: 
            cls.__instance = super().__new__(cls)
        return cls.__instance 
    
    def __init__(self): 
        # 初始化 _type_mappings（如果尚未初始化）  
        if not Py2Sql._type_mappings: 
            self._init_py_type()
    
    def python_type_to_sql_type(self, python_type): 
        return self.__python_type_to_sql_type0(python_type)

    def __python_type_to_sql_type0(self, python_type): 
        
        if isinstance(python_type, String):
            # print(">>>>>>>>>>>>>>>>>>>>>>",python_type.len)
            # e.g. String(100)
            return self.__default_type() + f"({python_type.len})"
        
        #check for Python whether support Annotated or version <=3.8.10
        if Py2Sql.__import_check or Py2Sql.__ANNOTATED_SUPPORTED:
            try:
                Py2Sql.__import_check = False
                from typing import Annotated, get_origin, get_args  
                Py2Sql.__ANNOTATED_SUPPORTED = True
            except ImportError:
                Py2Sql.__import_check = False
                Py2Sql.__ANNOTATED_SUPPORTED = False
                if not hasattr(Py2Sql, '_error_printed'):
                    print("\033[31m[ERROR] Note: Python's version<=3.8.10 do not support Annotated,get_origin and get_args! \033[0m ")  
                    Py2Sql._error_printed = True  # 设置类变量，标记错误消息已打印 
        
        # 获取复合类型的基本类型。
        if Py2Sql.__ANNOTATED_SUPPORTED:
            if get_origin(python_type) is Annotated:
                base_type, *annotations = get_args(python_type)  
                if base_type is str: 
                    # 提取字符串长度注解  
                    for annotation in annotations: 
                        if isinstance(annotation, str):
                            annotation = annotation.replace(" ", "")
                            if (annotation.startswith("length=") or annotation.startswith("len=")):
                                length = int(annotation.split("=")[1]) 
                                return self.__default_type() + f"({length})"  
                return self.python_type_to_sql_type(base_type)
        
        type_mapping = Py2Sql._type_mappings.get(HoneyContext.get_dbname(), Py2Sql._type_mappings["COMMON"])
  
        return type_mapping.get(python_type, self.__default_type() + "(255)")  
    
    def __default_type(self):
        if HoneyContext.isOracle():
            return "VARCHAR2"
        else:
            return "VARCHAR"  # 默认使用 VARCHAR 
    
    def _init_py_type(self):
        
        common_type_mappings: Dict[type, str] = {  
            str: "VARCHAR(255)",
            
            set: "TEXT",
            dict: "JSON",
            list: "TEXT",
            tuple: "TEXT",
            
            Set: "TEXT",
            Dict: "JSON",
            List: "TEXT",
            Tuple: "TEXT",
            
            decimal.Decimal:"Numeric",
            
            # 如果需要，可以加入支持的类型  
            String: "VARCHAR(255)",
            
            type(None): "VARCHAR(255)",
        }  
      
        Py2Sql._type_mappings: Dict[str, Dict[type, str]] = {
              
            DatabaseConst.MYSQL.lower(): {
                **common_type_mappings,  # 引用公共类型映射  
                int: "INT(11)",
                float: "FLOAT(19,6)",
                bool: "TINYINT(1)",
     
                date: "DATETIME",
                time: "TIME",
                datetime: "DATETIME",
                
                bytes:"BIT(64)"
            },
            DatabaseConst.MariaDB.lower(): {
                **common_type_mappings,  # 引用公共类型映射  
                int: "INT(11)",
                float: "FLOAT(19,6)",
                bool: "TINYINT(1)",
     
                date: "DATETIME",
                time: "TIME",
                datetime: "DATETIME",
                
                bytes:"BIT(64)"
            },
            DatabaseConst.ORACLE.lower(): { 
                **common_type_mappings,  # 引用公共类型映射
                int: "NUMBER(10)",
                float: "NUMBER(19,6)",
                bool: "VARCHAR2(1)",
     
                date: "DATE",
                time: "DATE",
                datetime: "DATE",
                
                str: "VARCHAR2(255)",
                type(None): "VARCHAR2(255)",
            },
            DatabaseConst.PostgreSQL.lower(): { 
                **common_type_mappings,  # 引用公共类型映射 
                int: "INT4",
                float: "FLOAT4",
                bool: "BIT",
                  
                date: "DATE",
                time: "TIME",  # Adjust according to PostgreSQL's time type  
                datetime: "TIMESTAMP",  # Or "TIMESTAMPTZ" for timezone-aware  
            },
            DatabaseConst.SQLite.lower():{
                **common_type_mappings,  # 引用公共类型映射
                int: "int(11)",
                float: "FLOAT4",
                bool: "BOOLEAN",
                
                date: "DATETIME",  # 日期字段  
                time: "VARCHAR(8)",
                datetime: "DATETIME",  # 日期时间字段 
            },
            DatabaseConst.H2.lower():{
                **common_type_mappings,  # 引用公共类型映射
                int: "INT4",
                float: "FLOAT4",
                bool: "BIT",
                
                date: "DATETIME",  # 日期字段  
                time: "VARCHAR(8)",
                datetime: "DATETIME",  # 日期时间字段 
            
                str: "VARCHAR2(255)",
                type(None): "VARCHAR2(255)",
            },
            DatabaseConst.SQLSERVER.lower():{
                **common_type_mappings,  # 引用公共类型映射
                int: "int",
                float: "real",
                bool: "char(1)",
                
                date: "datetime",  # 日期字段
                time: "time",
                datetime: "datetime",  # 日期时间字段 
            
                str: "nvarchar(255)",
                type(None): "nvarchar(255)",
            },
            "COMMON":{
                **common_type_mappings,  # 引用公共类型映射
                int: "int(11)",
                float: "FLOAT",
                bool: "BOOLEAN",
                
                date: "DATE",  # 日期字段  
                time: "VARCHAR(8)",  # 日期字段  #todo
                # time: "TIME",  # 日期字段  
                datetime: "DATETIME",  # 日期时间字段
            },
            
        }
              
        """将 Python 类型映射到 SQL 类型，支持字符串长度和时间字段"""  


class Sql2Py:
    __instance = None
    
    _sql_type_mappings: Dict[str, Dict[str, str]] = {}
    # common_sql_type_mappings: Dict[str, str] = {}
    
    def __new__(cls): 
        if cls.__instance is None: 
            cls.__instance = super().__new__(cls)
        return cls.__instance 
    
    def __init__(self): 
        # 初始化 _db_sql（如果尚未初始化）  
        if not Sql2Py._sql_type_mappings: 
            self._init_sql_type()
    
    def sql_type_to_python_type(self, sql_type): 
        type_mapping = Sql2Py._sql_type_mappings.get(HoneyContext.get_dbname(), Sql2Py._sql_type_mappings["COMMON"]) 
        
        py_type = type_mapping.get(sql_type.lower(), type_mapping.get(sql_type.upper()))
        if py_type is None:
            py_type = "str"
        return py_type
    
    def _init_sql_type(self):
    
        common_sql_type_mappings: Dict[str, str] = {
            "VARCHAR":"str",
            "TEXT":"str",
            "JSON":"str",
            "VARCHAR":"str",
            "VARCHAR(255)":"str",
            "int":"int",
            "INT":"int",
            "BIGINT":"int",
            
            "INTEGER":"int",
            "BOOLEAN":"bool",
            "BLOB":"bytes",
            "REAL":"float",
            
            # None: "str",
        }  
      
        Sql2Py._sql_type_mappings: Dict[str, Dict[str, str]] = {
              
            DatabaseConst.MYSQL.lower(): {
                **common_sql_type_mappings,  # 引用公共类型映射  
                "TINYINT":"bool",
                "DATETIME":"date",
                "TIME":"time",
                "DATETIME":"datetime",
                "BIT":"bytes",  # 要判断长度 ？
                "FLOAT":"float",
            },
            DatabaseConst.MariaDB.lower(): {
                **common_sql_type_mappings,  # 引用公共类型映射  
                "TINYINT":"bool",
                "DATETIME":"date",
                "TIME":"time",
                "DATETIME":"datetime",
                "BIT":"bytes",  # 要判断长度 ？
                "FLOAT":"float",
            },
            DatabaseConst.ORACLE.lower(): {
                 
                **common_sql_type_mappings,  # 引用公共类型映射
                "NUMBER(10)":"int",
                "NUMBER(19,6)":"float",  # 要使用长度？  todo
                "NUMBER":"int",
                "VARCHAR2(1)":"bool",
                "VARCHAR2":"str",
                "DATE":"datetime",
            },
            DatabaseConst.PostgreSQL.lower(): { 
                **common_sql_type_mappings,  # 引用公共类型映射 
                "FLOAT4":"float",
                "INT4":"int",
                "BIT":"bool",
                
                "DATE":"date",
                "TIME":"time",
                "TIMESTAMP":"datetime",
            },
            DatabaseConst.SQLite.lower():{
                **common_sql_type_mappings,  # 引用公共类型映射
                "FLOAT4":"float",
                "INT4":"int",
                "int(11)":"int",
                "BOOLEAN":"bool",
                "DATETIME":"datetime",
            },
            DatabaseConst.H2.lower():{
                **common_sql_type_mappings,  # 引用公共类型映射
                "VARCHAR2":"str",
                "DATETIME":"datetime",
                "BIT":"bool",
                "FLOAT4":"float",
                "INT4":"int",
            },
            DatabaseConst.SQLSERVER.lower():{
                **common_sql_type_mappings,  # 引用公共类型映射
                "real":"float",
                "nvarchar":"str",
                "char(1)":"bool",
                "char":"str",
                "datetime":"datetime",
                "time":"time",
            },
            "COMMON":{
                **common_sql_type_mappings,  # 引用公共类型映射
                "INTEGER":"int",
                "FLOAT":"float",
                "BOOLEAN":"bool",
                "DATE":"date",
                "DATETIME":"datetime",
            },
        }
        
        
class Mid:
    __instance = None
    
    _mid_to_py_mappings: Dict[str, type] = {}
    _mid_to_sqltype_mappings: Dict[str, Dict[str, str]] = {}
    
    def __new__(cls): 
        if cls.__instance is None: 
            cls.__instance = super().__new__(cls)
        return cls.__instance 
    
    def __init__(self): 
        # 初始化 _db_sql（如果尚未初始化）  
        if not Mid._mid_to_py_mappings: 
            self._init_type()
        if not Mid._mid_to_sqltype_mappings:
            self._init_mid_to_sqltype()
        
    def _init_type(self): 
        
        #2 mid -> py type
        Mid._mid_to_py_mappings: Dict[str, str] = {
            "String":str,
            "Text":str,
            "JSON":str,
            "VARCHAR":str,
            "Integer":int,
            "BigInteger":int,
            # "SmallInt":int,
            "SmallInteger":int,
            "DateTime":datetime,
            "Date":date,
            "Time":time,
            
            "Float":float,
            "Numeric":decimal.Decimal,
            "DECIMAL":decimal.Decimal,
            
            "Boolean":bool,
            "REAL":float,
            
            None: str,
        }
        
    def mid_to_python_type(self, mid_type): 
        return Mid._mid_to_py_mappings.get(mid_type, str)
    
    def mid_to_sqltype(self, mid_type):
        
        type_mapping = Mid._mid_to_sqltype_mappings.get(HoneyContext.get_dbname(), Mid._mid_to_sqltype_mappings["COMMON"]) 
        
        sql_type = type_mapping.get(mid_type.lower(), type_mapping.get(mid_type.upper(), None))
        return sql_type
    
    #1 mid->sql type   mid到SQL直接映射
    def _init_mid_to_sqltype(self):  

        common_type_mappings: Dict[str, str] = {
            "string":"varchar",
            "text":"text",
            "JSON":"text",
            "varchar":"varchar(255)",

            "integer":"int",
            # "smallint":"smallint",
            "smallinteger":"smallint",
            "biginteger":"bigint",

            "datetime":"DateTime",
            "date":"Date",
            "time":"Time",

            "float":"float",
            "numeric":"Numeric",

            "boolean":"boolean",
            "real":"float",
        }
        Mid._mid_to_sqltype_mappings: Dict[str, Dict[str, str]] = {

            DatabaseConst.MYSQL.lower(): {
                **common_type_mappings,  # 引用公共类型映射  
                "int": "INT(11)",
                "float": "FLOAT(19,6)",
                "boolean": "TINYINT(1)",
                "JSON":"JSON",

                "date": "DATETIME",
                "time": "TIME",
                "datetime": "DATETIME",
            },
           DatabaseConst.MariaDB.lower(): {
                **common_type_mappings,  # 引用公共类型映射  
                "int": "INT(11)",
                "float": "FLOAT(19,6)",
                "boolean": "TINYINT(1)",
                "JSON":"JSON",

                "date": "DATETIME",
                "time": "TIME",
                "datetime": "DATETIME",
            },
            DatabaseConst.ORACLE.lower(): { 
                **common_type_mappings,  # 引用公共类型映射

                "string":"VARCHAR2",
                "text":"VARCHAR2",
                "JSON":"VARCHAR2",
                "VARCHAR":"VARCHAR2",

                "biginteger":"NUMBER(19)",
                "integer":"NUMBER(10)",
                "smallint":"number(5)",
                "smallinteger":"number(5)",
                "datetime":"DATE",
                "date":"DATE",
                "time":"DATE",

                "float":"NUMBER(19,6)",
                "numeric":"NUMBER",

                "boolean":"VARCHAR2(1)",
                "real":"float",
            },
            DatabaseConst.PostgreSQL.lower(): { 
                **common_type_mappings,  # 引用公共类型映射 
                "int": "INT4",
                "float": "FLOAT4",
                "boolean": "BIT",
            
                "date": "DATE",
                "time": "TIME",  # Adjust according to PostgreSQL's time type  
                "datetime": "TIMESTAMP",  # Or "TIMESTAMPTZ" for timezone-aware  
            },
            DatabaseConst.SQLite.lower():{
                **common_type_mappings,  # 引用公共类型映射
                "int": "int(11)",
                "float": "FLOAT4",
            
                "date": "DATETIME",  # 日期字段  
                "time": "VARCHAR(8)",
                "datetime": "DATETIME",  # 日期时间字段 
            },
            DatabaseConst.H2.lower():{
                **common_type_mappings,  # 引用公共类型映射
                "int": "INT4",
                "float": "FLOAT4",
                "boolean": "BIT",
            
                "date": "DATETIME",  # 日期字段  
                "time": "VARCHAR(8)",
                "datetime": "DATETIME",  # 日期时间字段 
            
                "string": "VARCHAR2",
            },
            DatabaseConst.SQLSERVER.lower():{
                **common_type_mappings,  # 引用公共类型映射
                "int": "int",
                "float": "real",
                "boolean": "char(1)",
            
                "date": "datetime",  # 日期字段
                "time": "time",
                "datetime":"datetime",  # 日期时间字段 
            
                "string": "nvarchar",
            },
            "COMMON":{
                **common_type_mappings,  # 引用公共类型映射
                "time": "VARCHAR(8)",  # 日期字段  #todo
            },
        }
        
#sql/sqltypes.py       
# Integer: 整数类型。
# SMALLINT  
# SmallInteger: 小整数类型，范围较小。
# BigInteger: 大整数类型，范围更大。
# Float: 浮点数类型。
# Numeric: 精确的小数类型，支持定制精度和标度。
# String(length): 字符串类型，可以指定长度。
# Text: 大文本类型，不限制长度。
# Boolean: 布尔类型，True 或 False。
# Date: 日期类型，不包含时间。
# Time: 时间类型，不包含日期。
# DateTime: 日期和时间类型。
# Interval: 时间间隔类型。
# PickleType: 可序列化的 Python 对象类型。
# LargeBinary: 二进制数据，适合存储大块数据。
#
# JSON: JSON 数据类型，适用于存储 JSON 格式的数据。
# ARRAY: 数组类型，适用于 PostgreSQL 等支持数组的数据库。
# Enum: 枚举类型，限制到特定的字符串值集合。
# ForeignKey: 外键类型，用于定义模型之间的关联。
        
