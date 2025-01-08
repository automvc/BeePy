'''
标准get,set Bean
有构造方法

 get/set 还要测试没有构造方法的。  可以的
'''

class Orders42: 
    __tablename__ = 'orders'  

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
