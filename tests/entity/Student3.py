class Student3:
    id:int = None
    name = None 
    age:int = None  
    remark = None
    addr = None

    def __repr__(self): 
        return  str(self.__dict__)
