from bee.api import SuidRich

import MyConfig
from entity.Orders import Orders
from entity.Orders3 import Orders3
from entity.Student2 import Student2
from entity.Student3 import Student3
from entity.full import Entity


# from bee.util import HoneyUtil
if __name__ == '__main__':

    # create_sql=HoneyUtil.get_create_sql(Entity)
    
    MyConfig.init()
    suidRich = SuidRich()
    
    #有声明类型和无声明类型都有
    suidRich.create_table(Entity,True)
    
    #无声明类型
    suidRich.create_table(Orders,True)
    
    # suidRich.create_table(Orders3,True)
    
    # suidRich.create_table(Student2,True)
    # suidRich.create_table(Student3,True)