from bee.api import Suid

import MyConfig
from entity.Orders4 import Orders4


# from bee.HoneyUtil import HoneyUtil
# 实例化对象  
if __name__ == '__main__':  
    MyConfig.init()
    
    # orders = Orders4(id=1, name="bee")  
    orders = Orders4(name="bee")
    
    # 使用Setter设置属性  
    # orders.remark = 'test'  
    
    print(orders.__dict__)
        
    print("start")
    
    suid = Suid()
    #select name, remark, id from orders where name = ?   TODO类级别的属性，要不要转到这？？？
    # V1.x 暂时不支持获取get/set Bean的类级别属性(作为条件等)。
    orderList = suid.select(orders)
    # print(orderList)
    if orderList is not None:
        # print(orderList)
        for one in orderList: 
            # print(one.id) 
            # print(one.name)  
            print(one)
    else:
        print(" --no data!")
    
    print("---finished")
