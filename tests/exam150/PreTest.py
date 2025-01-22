from bee.api import PreparedSql
from bee.config import PreConfig
from entity.Orders import Orders


if __name__=="__main__":
    
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    pre=PreparedSql()
    
    # pre.select("select * from orders", "Orders", params=["active"],  start=1,size=10)
    # pre.select("select * from orders where name=?", Orders, params=["bee"])
    # pre.select("select * from orders where name=?", Orders, params=["bee"],  size=10)
    # one =pre.select("select * from orders where name=?", Orders, params=["bee"],  start=1)
    # print(one)
    print("-------------------")
    one =pre.select("select * from orders", Orders)
    print(one)
    print("-------------------")
    one =pre.select("select * from orders", Orders,size=2)
    print(one)
    print("finished")
