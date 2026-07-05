import random

from bee.api import SuidRich
from bee.config import HoneyConfig

import MyConfig
from entity.Orders import Orders


#custom way set db config
if __name__ == '__main__':
    print("start")
    
    # MyConfig.init()
    
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
    
    suidRich = SuidRich()
    # x = random.random()  # 0.0 <= x < 1.0
    x = random.randint(0, 1000)  # a <= n <= b（包含两端）
    orders = Orders()
    orders.name = "bee-" + str(x)
    
    suidRich.insert(orders)
    
    one = suidRich.select(orders)
    
    print(one)
    
    print("finished")
