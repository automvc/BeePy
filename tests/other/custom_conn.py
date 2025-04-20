from bee.api import SuidRich
from bee.config import HoneyConfig
from bee.factory import BeeFactory
import pymysql

from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    
    config = {  
        # 'dbName':'MySQL',
        'host': 'localhost',  # 数据库主机  
        'user': 'root',  # 替换为您的 MySQL 用户名  
        'password': '',  # 替换为您的 MySQL 密码  
        'database': 'bee',  # 替换为您的数据库名称  
        'port':3306
    }
    
    honeyConfig= HoneyConfig()
    honeyConfig.set_dbname("MySQL")
    
    conn = pymysql.connect(**config)
    factory=BeeFactory()
    factory.set_connection(conn)
    
    
    orders=Orders()
    # orders.name = "bee"
    
    suidRich = SuidRich()
    orderList = suidRich.select(orders)
    
    for one in orderList: 
        print(one)  
    
    print("finished")