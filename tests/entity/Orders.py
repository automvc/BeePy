'''

这种可以不需要构造方法。
不写属性的类型

Created on 2024年10月19日

@author: Bee
'''

class Orders:
    #__tablename__="orders6"
    id = None  
    name = None 
    type = None
    remark = None
    
    # __pk__="id" 
    # __pk__ = "name"  
    # __primary_key__="name" 
    __unique_key__={"name"}
    __not_null_filels__={"name"} # "id"不用设置

    #can ignore
    def __repr__(self):  
        return  str(self.__dict__)

