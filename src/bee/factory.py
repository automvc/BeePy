from bee.osql.honeyfactory import HoneyFactory

class BeeFactory:
    
    __connection = None
    
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None: 
            cls.__instance = super().__new__(cls)
        return cls.__instance 
        
    def set_connection(self, connection):
        BeeFactory.__connection = connection
    
    def get_connection(self):
        return BeeFactory.__connection
    
    # def __getattribute__(self, item):  
    #     print(f"Accessing attribute: {item}") 
    #     return super().__getattribute__(item)
    
    
    def getHoneyFactory(self):
        return HoneyFactory()
    