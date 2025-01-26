'''
标准get,set Bean, 但有类级属性
有构造方法

get/set 还要测试没有构造方法的。  在Orders42,是可以的。
'''

class Orders4: 
    __tablename__ = 'orders' 
    
    #可以有属性也可以没有  
    # V1.x 暂时不支持获取get/set Bean的类级别属性(作为条件等)。
    name = None
    remark="test2"

    #可以有构造方法，也可以没有
    def __init__(self, id: int=None, name: str=None, remark: str=None): 
        self._id = id  
        self._name = name  
        self._remark = remark  

    # Getter 和 Setter 方法  
    @property  
    def id(self): 
        return self._id  

    @id.setter  
    def id(self, value): 
        self._id = value  

    @property  
    def name(self): 
        return self._name  

    @name.setter  
    def name(self, value): 
        self._name = value  

    @property  
    def remark(self): 
        return self._remark  
    
    @remark.setter  
    def remark(self, value): 
        self._remark = value  
        
    def __repr__(self): 
        return  str(self.__dict__)
