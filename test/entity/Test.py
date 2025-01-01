'''
Created on 2024年10月19日

'''
class Test:
    id: int = None
    name: str = None
    
    # def __init__(self, id=None, name=None):  
    #     self.id = id  
    #     self.name = name  

    def __repr__(self):  
        # return f"Order(id={self.id}, name='{self.name}')"  
        return  str(self.__dict__)

