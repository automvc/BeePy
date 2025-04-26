from bee.api import SuidRich
from bee.config import HoneyConfig
from bee.osql.obj2sql import ObjToSQL

import MyConfig
from entity.Orders import Orders
from entity.Orders3 import Orders3
from entity.Student2 import Student2
from entity.Student3 import Student3
from entity.Test import Test
from entity.full import Entity


# from bee.util import HoneyUtil
if __name__ == '__main__':

    # create_sql=HoneyUtil.get_create_sql(Entity)
    
    MyConfig.init()
    suidRich = SuidRich()
    
    #有声明类型和无声明类型都有
    # suidRich.create_table(Entity,True)
    
    #无声明类型
    suidRich.create_table(Orders,True)
    suidRich.create_table(Test,True)
    
    ######1. just print create table sql
    # honeyConfig = HoneyConfig()
    # # honeyConfig.set_dbname("MySQL")
    # # # honeyConfig.set_dbname("Oracle")
    # # # honeyConfig.set_dbname("sqlite")
    # honeyConfig.set_dbname("H2")
    # sql = ObjToSQL().toCreateSQL(Orders)
    # print(sql)
    
    # suidRich.create_table(Orders3,True)
    
    # suidRich.create_table(Student2,True)
    # suidRich.create_table(Student3,True)
