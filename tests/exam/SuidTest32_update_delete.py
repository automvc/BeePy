from bee.api import Suid

import MyConfig
from entity.Orders3 import Orders3


# from entity import Orders3
# from bee.HoneyUtil import HoneyUtil
if __name__ == '__main__':
    print("start")
    MyConfig.init()
    # orders=Orders(id=1, name="bee")
    orders=Orders3()
    orders.name="bee130"
    # orders.remark=None
    orders.ext="aaa"  #实体没有字段，会被忽略。出于安全考虑
    
    # print(orders.__dict__)
    # {'id': None, 'name': 'bee', 'remark': None, 'ext': 'aaa'}
    
    orders.id=10002
    
    suid = Suid()
    n1= suid.update(orders)
    n2= suid.delete(orders)
    print(n1)
    print(n2)
    # orderList = suid.select(orders)
    orderList = suid.select(Orders3())
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
