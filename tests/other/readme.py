class Orders:
    id = None  
    name = None 
    remark = None

    #can ignore
    def __repr__(self):  
        return  str(self.__dict__)
  
#also can use field type as :int        
class Orders8:
    __tablename__ = "orders"
    id:int = None  
    name:str = None 
    remark:str = None

    def __repr__(self): 
        return  str(self.__dict__)
        
class Student2:
    id = None
    name = None 
    age = None  
    remark = None
    addr = None

    def __repr__(self): 
        return  str(self.__dict__)
        
        
from bee.api import Suid, SuidRich
from bee.config import PreConfig


if __name__=="__main__":

    #set bee.properties/bee.json config folder
    PreConfig.config_path="E:\\Bee-Project"

    # select record
    suid=Suid()
    orderList=suid.select(Orders()) #select all
    
    #insert    
    orders=Orders()
    orders.id=1
    orders.name="bee"
    orders.remark="test"
    
    suid=Suid()
    suid.insert(orders)
    
    #update/delete
    orders=Orders()
    orders.name="bee130"
    #For safety reasons
    #Fields that are not present in the entity will be ignored.
    orders.ext="aaa"  
    orders.id=1
    
    suid = Suid()
    n1= suid.update(orders)
    n2= suid.delete(orders)
    print(n1)
    print(n2)
    
    #batch insert
    student0=Student2()
    student0.name = "bee"
    student1=Student2()
    student1.name = "bee1"
    student1.addr=""
    student1.age=40
    entity_list=[]
    entity_list.append(student0)
    entity_list.append(student1)
    
    suidRich = SuidRich()
    insertNum = suidRich.insert_batch(entity_list)
    print(insertNum)
    
    #SuidRich: insert_batch,select_first,updateBy
    #complex where statement constructor Condition