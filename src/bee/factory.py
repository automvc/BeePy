from bee.config import HoneyConfig
from bee.name.naming import NameTranslate, UnderScoreAndCamelName, \
    UpperUnderScoreAndCamelName, OriginalName, DbUpperAndPythonLower


class BeeFactory:
    
    __connection = None
    
    __instance = None
    __honeyFactory = None
    
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
        #     (DB<-->Python),
        # 1: order_no<-->orderNo 
        # 2: ORDER_NO<-->orderNo
        # 3: original,
        # 4: ORDER_NO<-->order_no (DbUpperAndPythonLower)
        if self.__nameTranslate is None:
            translateType = HoneyConfig.naming_translate_type
            if translateType == 1: __nameTranslate = UnderScoreAndCamelName()
            elif translateType == 2: __nameTranslate = UpperUnderScoreAndCamelName()
            elif translateType == 3: __nameTranslate = OriginalName()
            elif translateType == 4: __nameTranslate = DbUpperAndPythonLower()
            else:__nameTranslate = UnderScoreAndCamelName()
                
        return __nameTranslate
    
    # def __getattribute__(self, item):  
    #     print(f"Accessing attribute: {item}") 
    #     return super().__getattribute__(item)
    
    # def getHoneyFactory(self):
    #     if self.__honeyFactory is None:
    #         __honeyFactory = HoneyFactory()
    #     return __honeyFactory
    
