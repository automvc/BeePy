import MyConfig
from bee.honeyfactory import BF
from entity.Orders import Orders


#test cache    
if __name__ == '__main__':
    print("start")
    
    MyConfig.init()
    
    # orders=Orders()
    # # orders = Test()
    # orders.id=1
    # orders.name = "bee"
    
    orders=""  #test empty string entity
    suid = BF.suid()
    orderList = suid.select(orders) #test 
    if orderList:
        for one in orderList: 
            print(one)
    else:
        print("empty result")
        
    orderList = suid.select(None) #test 
    if orderList:
        for one in orderList: 
            print(one)
    else:
        print("empty result")