'''

这种可以不需要构造方法。
不写属性的类型

Created on 2025年02月03日

@author: Bee
'''

class Orders_202501:
    # id = None  
    name = None 
    remark = None
    type = None

    #can ignore
    def __repr__(self):  
        return  str(self.__dict__)

