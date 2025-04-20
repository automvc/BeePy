class Orders:
    #__tablename__="orders6"
    id = None  
    name = None 
    remark = None
    # remark: str = None  
    
    # __pk__="id" #aaa
    # __pk__ = "name"  # aaa
    # __primary_key__="name" #aaa

    #can ignore
    def __repr__(self):  
        return  str(self.__dict__)
    
    
if __name__ == '__main__':
    print("start")
    
    # MyConfig.init()
    
    # orders=Orders()
    # orders.name = "bee"
    anno={}
    try:
        anno =Orders.__annotations__
    except Exception:
        pass
        
    print(anno)    
       
    
    print("finished")
