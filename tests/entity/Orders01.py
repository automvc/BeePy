'''
_单下划线
这种可以不需要构造方法。
不写属性的类型

Created on 2024年10月19日

'''

class Orders:

    _id = None  
    _name = None 
    _remark = None
    

    def __repr__(self):  
        # return f"Orders(id={self.id}, name='{self.name}')"  
        return  str(self.__dict__)

