from bee.api import PreparedSql

import MyConfig
from entity.Orders import Orders


if __name__=="__main__":
    
    MyConfig.init()
    
    pre=PreparedSql()
    
    # pre.select("select * from orders", "Orders", params=["active"],  start=1,size=10)
    # pre.select("select * from orders where name=?", Orders, params=["bee"])
    # pre.select("select * from orders where name=?", Orders, params=["bee"],  size=10)
    # one =pre.select("select * from orders where name=?", Orders, params=["bee"],  start=1)
    # print(one)
    print("-------------------")
    listEntity = pre.select("select * from orders", Orders)
    print(listEntity)
    print("-------------------")
    listEntity = pre.select("select * from orders", Orders, size=2)
    print(listEntity)
    
    listEntity = pre.select("select * from orders", Orders, start=2)
    print(listEntity)
    print("finished")
