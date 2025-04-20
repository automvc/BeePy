# from bee.config import HoneyConfig
# from bee.osql.const import DatabaseConst

import MyConfig
from bee.gen import GenBean


if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    gen = GenBean()
    # gen.gen_bean("test_name") 
    
    path="E:\\xxx\\BeePy\\tests"
    gen.gen_and_write_bean("test_name", path)
    
    # #test custom add fetch_bean_sql
    # sql="SELECT column_name col, data_type type, nullable ynNull, data_default defaultValue, data_length strLen  FROM user_tab_columns  WHERE table_name = UPPER('{table_name}') ORDER BY column_id"
    # GenBean.add_fetch_bean_sql(DatabaseConst.ORACLE, sql)
    # HoneyConfig().set_dbname(DatabaseConst.ORACLE)
    # custom_sql=gen._get_fetch_bean_sql("abc")
    # print(custom_sql)
    
    print("finished")
