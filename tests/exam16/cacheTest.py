import MyConfig
from bee.honeyfactory import BF
from entity.Orders import Orders


#test cache    
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    orders=Orders()
    # orders = Test()
    orders.id=1
    orders.name = "bee"
    
    suid = BF.suid()
    orderList = suid.select(orders) #test 
    for one in orderList: 
        print(one)
    
    #test cache    
    orderList = suid.select(orders) #test 
    for one in orderList: 
        print(one)
    
    orders2=Orders()
    orders2.id=2
    orders2.name = "bee2"
    suid.insert(orders2)
        
    #test cache    
    orderList = suid.select(orders) #test 
    for one in orderList: 
        print(one)
        
    # condition = BF.condition()  
    # condition.op("name", Op.ne, "bee1").op("remark", Op.ne, "new2")
    # orderList = suid.select(orders,condition)
    # for one in orderList: 
    #     print(one)
        
        
        
       
    
    print("finished")
