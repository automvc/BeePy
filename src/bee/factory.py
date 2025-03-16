# from bee.honeyfactory import HoneyFactory
from bee.name.naming import *


class BeeFactory:
    
    __connection = None
    
    __instance = None
    __honeyFactory=None
    
    def __new__(cls):
        if cls.__instance is None: 
            cls.__instance = super().__new__(cls)
        return cls.__instance 
        
    def set_connection(self, connection):
        BeeFactory.__connection = connection
    
    def get_connection(self):
        return BeeFactory.__connection
    
    
    __nameTranslate = None
    
    def getInitNameTranslate(self) -> NameTranslate:
        
        if self.__nameTranslate is None:
            # int translateType=HoneyConfig.getHoneyConfig().naming_translateType;
            translateType = 1  # TODO from config
            if translateType == 1: __nameTranslate = UnderScoreAndCamelName()
            elif translateType == 2: __nameTranslate = UpperUnderScoreAndCamelName()
            elif translateType == 3: __nameTranslate = OriginalName()
            elif translateType == 4: __nameTranslate = DbUpperAndJavaLower()
            else:__nameTranslate = UnderScoreAndCamelName()
                
        return __nameTranslate;
    
    # def __getattribute__(self, item):  
    #     print(f"Accessing attribute: {item}") 
    #     return super().__getattribute__(item)
    
    # def getHoneyFactory(self):
    #     if self.__honeyFactory is None:
    #         __honeyFactory = HoneyFactory()
    #     return __honeyFactory
    


    
