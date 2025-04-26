# from bee.config import HoneyConfig
# from bee.osql.const import DatabaseConst

from bee.config import HoneyConfig
from bee.gen import GenBean

import MyConfig


if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    gen = GenBean()
    # gen.gen_bean("test_name") 
    
    path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests"
    # gen.gen_and_write_bean("test_name", path)
    
    # #test custom add fetch_bean_sql
    # sql="SELECT column_name col, data_type type, nullable ynNull, data_default defaultValue, data_length strLen  FROM user_tab_columns  WHERE table_name = UPPER('{table_name}') ORDER BY column_id"
    # GenBean.add_fetch_bean_sql(DatabaseConst.ORACLE, sql)
    # HoneyConfig().set_dbname(DatabaseConst.ORACLE)
    # custom_sql=gen._get_fetch_bean_sql("abc")
    # print(custom_sql)
    
    
    # honeyConfig = HoneyConfig()
    # # honeyConfig.set_dbname("MySQL")
    # # honeyConfig.set_dbname("Oracle")
    # # honeyConfig.set_dbname("sqlite")
    # honeyConfig.set_dbname("H2")
    # gen._get_fetch_bean_sql("test_name")
    
    print("finished")
