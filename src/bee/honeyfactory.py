from bee.api import Suid, SuidRich, PreparedSql

from bee.condition import ConditionImpl
from bee.osql.obj2sql import ObjToSQL
from bee.osql.sqllib import BeeSql


class HoneyFactory:
    
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None: 
            cls.__instance = super().__new__(cls)
        return cls.__instance 
    
    def __init__(self): 
        self.suid = None  
        self.suidRich = None  
        self.beeSql = None  
        self.objToSQL = None  
        self.preparedSql = None  
        self.condition = None  
    
    def getSuid(self): 
        if self.suid is None: 
            return Suid()  
        return self.suid  
    
    def setSuid(self, suid): 
        self.suid = suid  
    
    def getSuidRich(self): 
        if self.suidRich is None: 
            return SuidRich()
        return self.suidRich  
    
    def setSuidRich(self, suidRich): 
        self.suidRich = suidRich  
    
    def getBeeSql(self): 
        if self.beeSql is None: 
            return BeeSql()  
        return self.beeSql  
    
    def setBeeSql(self, beeSql): 
        self.beeSql = beeSql  
    
    def getObjToSQL(self): 
        if self.objToSQL is None: 
            return ObjToSQL()  
        return self.objToSQL  
    
    def setObjToSQL(self, objToSQL): 
        self.objToSQL = objToSQL  
    
    def getPreparedSql(self): 
        if self.preparedSql is None: 
            return PreparedSql()  
        return self.preparedSql  
    
    def setPreparedSql(self, preparedSql): 
        self.preparedSql = preparedSql  
    
    def getCondition(self): 
        if self.condition is None: 
            return ConditionImpl()  
        return self.condition  
    
    def setCondition(self, condition): 
        if condition is not None: 
            # self.condition = condition.clone()  
            self.condition = condition
        else: 
            self.condition = condition 
    
    
class BF:

    @staticmethod
    def suid():
        return HoneyFactory().getSuid()

    @staticmethod
    def suidRich():
        return HoneyFactory().getSuidRich()

    @staticmethod
    def condition():
        return HoneyFactory().getCondition()
    
    @staticmethod
    def preparedSql():
        return HoneyFactory().getPreparedSql()
    
    @staticmethod
    def objToSQL():
        return HoneyFactory().getObjToSQL()
    
