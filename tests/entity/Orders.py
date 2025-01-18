'''

这种可以不需要构造方法。
不写属性的类型

Created on 2024年10月19日

@author: Bee
'''

class Orders:
    id = None  
    name = None 
    remark = None

    #can ignore
    def __repr__(self):  
        return  str(self.__dict__)

