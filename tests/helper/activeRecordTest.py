import MyConfig
from bee.active_record import BaseMode


class Orders8:
    __tablename__ = "orders"
    id:int = None  
    name:str = None 
    remark:str = None

    def __repr__(self): 
        return  str(self.__dict__)
    
class Orders9(BaseMode):
    __tablename__ = "orders"
    id:int = None  
    name:str = None 
    remark:str = None

    def __repr__(self): 
        return  str(self.__dict__)


if __name__ == '__main__':
    print("start")
    MyConfig.init()
    
    # orders8 = Orders8()
    # suid = BF.suid()
    # suid.select(orders8)
    
    
    orders9 = Orders9()
    # orders9.name="aaa2"
    orderList=orders9.select()
    
    for one in orderList: 
        print(one)   
    
    
    one=orders9.select_by_id(1)
    print(one)
    
    
    
