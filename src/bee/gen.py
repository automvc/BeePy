from typing import Dict, Any

from bee.api import PreparedSql
from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.name.naming_handler import NamingHandler
from bee.osql import Util
from bee.osql.const import DatabaseConst, SysConst
from bee.osql.struct import TableMeta
from bee.util import HoneyUtil

from bee.custom import Custom


class GenBean:
    
    _db_sql: Dict[str, Any] = {}
    
    def __init__(self): 
        # 初始化 _db_sql（如果尚未初始化）  
        if not GenBean._db_sql: 
            self._init_db_sql()  
            
    def gen_bean(self, table_name:str):
        sql = self._get_fetch_bean_sql(table_name)

        tableMeta_list = self._get_table_metadata(sql)
        # for one in tableMeta_list:
        #     print(one)
            
        code = self._metadata_to_bean(table_name, tableMeta_list)
        # print(code)
        return code
        
    def gen_and_write_bean(self, table_name:str, file_path: str, file_name:str = None):
        code = self.gen_bean(table_name)
        if file_name is None:
            # className = NamingHandler.toEntityName(table_name)
            file_name = table_name + ".py"
        Util.write_to_file(file_path, file_name, code)
    
    def _init_db_sql(self): 
        sql_mysql = "SELECT COLUMN_NAME col, DATA_TYPE type, CASE IS_NULLABLE WHEN 'YES' THEN 1  ELSE 0  END AS ynNull, CASE COLUMN_KEY WHEN 'PRI' THEN 1  ELSE 0  END AS ynKey, COLUMN_COMMENT label,COLUMN_DEFAULT defaultValue,CHARACTER_MAXIMUM_LENGTH strLen, NUMERIC_PRECISION precision,NUMERIC_SCALE scale FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{database}' AND TABLE_NAME = '{table_name}' ORDER BY ORDINAL_POSITION"
        sql_sqlite = "select name col,type,[notnull] ynNull,pk ynKey,dflt_value defaultValue from pragma_table_info('{table_name}')"
        
        GenBean._db_sql[DatabaseConst.MYSQL.lower()] = sql_mysql
        GenBean._db_sql[DatabaseConst.SQLite.lower()] = sql_sqlite 
        
        sql_oralce = "SELECT column_name col, data_type type, nullable ynNull, data_default defaultValue, data_length strLen, data_precision precision, data_scale scale FROM user_tab_columns  WHERE table_name = UPPER('{table_name}') ORDER BY column_id"
        GenBean.add_fetch_bean_sql(DatabaseConst.ORACLE, sql_oralce)
    
    def _get_fetch_bean_sql(self, table_name):
        
        dbName = HoneyContext.get_dbname()
        database = HoneyConfig().get_db_config_dict().get('database')
        
        sql = GenBean._db_sql.get(dbName, None)
        if sql is None:
            sql = Custom.custom_get_fetch_bean_sql(dbName)
        
        sql = sql.replace('{table_name}', table_name)
        if database:
            sql = sql.replace('{database}', database)
            
        return sql
    
    @staticmethod
    def add_fetch_bean_sql(dbname:str, sql:str):
        GenBean._db_sql[dbname.lower()] = sql
    
    def _get_table_metadata(self, sql):
        old_naming_translate_type= HoneyConfig.naming_translate_type
        HoneyConfig.naming_translate_type=3
    
        pre = PreparedSql()
        tableMeta_list = pre.select(sql, TableMeta)
        
        # reset    
        HoneyConfig.naming_translate_type=old_naming_translate_type
    
        return tableMeta_list
    
    def _metadata_to_bean(self, table_name, tableMeta_list) -> str:
        """生成实体类代码"""  
        dt_set = set()
        
        className = NamingHandler.toEntityName(table_name)
        
        class_lines = [  
            f"class {className}:",
            f"    \"\"\" table {table_name} 's entity \"\"\""  
        ]  
        
        # 添加字段  
        # for col in metadata['columns']:  
        
        for tableMeta in tableMeta_list:
            # default = 'None' if tableMeta.ynNull else ''
            default = 'None'
            fieldName = NamingHandler.toFieldName(tableMeta.col)
            fieldType = HoneyUtil.sql_type_to_python_type(tableMeta.type)
            
            if tableMeta.ynKey:
                if fieldName != SysConst.id:
                    class_lines.insert(2, f"    {SysConst.pk} = \"{fieldName}\"")
            
            if fieldType in ['datetime', 'date', 'time']: 
                dt_set.add(fieldType)
                class_lines.append(f"    {fieldName}: {fieldType}")
            else: 
                class_lines.append(f"    {fieldName}: {fieldType} = {default}")  
        
        # 添加__repr__方法  
        class_lines.extend([  
            "",
            "    def __repr__(self):",
            "        return str(self.__dict__)"  
        ])  
        
        code = ""
        if dt_set:
            code = "from datetime import " + ", ".join(sorted(dt_set))
            code += "\n\n"
        # 生成完整代码  
        # code = "\n".join(sorted(imports)) + "\n\n"
        code += "\n".join(class_lines)  
        return code

