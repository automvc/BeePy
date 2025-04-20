
from bee.api import SuidRich
from bee.config import HoneyConfig

from entity.Orders import Orders

#custom way set db config
if __name__ == '__main__':
    print("start")
    
    # PreConfig.config_properties_file_name="aaaa.txt"
    
    config=HoneyConfig()
    
    # use this way for custom config define.
    dict_config={
                    "dbname":"SQLite",
                    "database":"E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\resources\\bee.db"
                }
    config.set_db_config_dict(dict_config)
    
    #error way
    # config.set_dbname('SQLite')
    # config.database ='E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\bee.db'
    
    orders=Orders()
    # orders.name = "bee"
    
    suidRich = SuidRich()
    one = suidRich.select(orders)
    
    print(one)
    
    print("finished")
