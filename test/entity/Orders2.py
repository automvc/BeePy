'''

这种可以不需要构造方法。
还写明属性的类型

Created on 2024年10月19日
'''
from dataclasses import dataclass, field  

@dataclass 
class Orders2:
    __tablename__="orders"
    # id: int = None
    # name: str = None
    id: int = field(default=None)  
    name: str = field(default=None)  
    remark: str = field(default=None)  
    
    # def __init__(self, id=None, name=None):  
    #     self.id = id  
    #     self.name = name  

    def __repr__(self):  
        # return f"Order(id={self.id}, name='{self.name}')"
        return  str(self.__dict__) 
    

