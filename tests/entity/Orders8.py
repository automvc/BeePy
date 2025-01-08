'''

这种可以不需要构造方法。
部分写属性的类型

Created on 2024年10月19日

'''


class Orders8:
    __tablename__ = "orders"
    id:int = None  
    name:str = None 
    remark:str = None

    def __repr__(self): 
        return  str(self.__dict__)

