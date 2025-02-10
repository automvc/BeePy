'''

对象有比类多属性；
默认对象多的属性将被忽略；因为不安全。

有构造方法

Created on 2024年10月19日
'''

class Orders3:
    __tablename__="orders"
    id = None  
    name = None
    remark="test" 
    
    # __pk__="name"
    # __pk__="id"
    
    def __init__(self, id=None,id2=None, name=None,remark=None):  
        self.id = id  
        self.id2=id2
        self.name = name 
        self.remark=remark 
        # 在 __init__ 方法中定义的 self.id, self.name, 和 self.remark 是实例属性。
        # 这意味着每个实例都会有这些属性，并且它们在创建实例时通过 __init__ 方法被初始化。
        #使用 orders=Orders3()也可以实例化，因为参数没传，就用默认值None

    def __repr__(self):  
        return  str(self.__dict__) 

