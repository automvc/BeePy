
import MyConfig
from bee.honeyfactory import BF
from entity.Orders import Orders


if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    orders=Orders()
    orders.name = "bee"
    
    suidRich = BF.suidRich()
    # orderList = suidRich.select(orders)
    orderList = suidRich.select_paging(orders, 0, 2, "id", "name")
    # orderList = suidRich.select_paging(orders, 0, 2, "id", "--name")
    # orderList = suidRich.select_paging(orders, 1, 0, "id", "name")
    # orderList = suidRich.select_paging(orders, "", 2, "id", "name")
    # orderList = suidRich.select_paging(orders,0,2)
    
    
    
    # condition=BF.condition()
    # condition.selectField("id","name")
    # condition.start(1).size(2)
    # orderList=suidRich.select(orders, condition)
    for one in orderList:
        print(one)
        
       
    
    print("finished")
