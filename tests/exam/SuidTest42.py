# from org.teasoft.exam.entity.Orders42 import Orders42
from bee.api import Suid

import MyConfig
from entity.Orders42 import Orders42


# from bee.HoneyUtil import HoneyUtil
# 实例化对象  
if __name__ == '__main__':  
    MyConfig.init()
    # orders = Orders42(id=1, name="bee")  
    
    orders = Orders42()
    # 使用Setter设置属性  
    # orders.remark = 'test'  
        
    print("start")
    
    suid = Suid()
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
