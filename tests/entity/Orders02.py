'''
__双下划线
这种可以不需要构造方法。
不写属性的类型

Created on 2024年10月19日

'''

class Orders:
    __id = None  
    __name = None 
    __remark = "init __remark"
    
    # def __init__(self, **kwargs):  
    #     for key, value in kwargs.items():  
    #         setattr(self, key, value)  
    
    # def __init__(self, id=None, name=None):  
    #     self.id = id  
    #     self.name = name  

    def __repr__(self):  
        # return f"Orders(id={self.id}, name='{self.name}')"  
        return  str(self.__dict__)

