from datetime import datetime 
import threading

from bee.osql.enum import SuidType
from bee.osql.logger import Logger

class AbstractCommOperate:
    
    def __init__(self):  
        self.local = threading.local()  # 初始化线程本地存储  

    def doBeforePasreEntity(self, entity, SuidType:SuidType):
        #子类在调用此方法时，记录当前的时间，_bee_base_t1
        show_sql_spent_time = False #TODO config
        if show_sql_spent_time:
            self.local._bee_base_t1 = datetime.now()
            
    def doBeforePasreListEntity(self, entityArray, SuidType:SuidType):
        show_sql_spent_time = False #TODO config
        if show_sql_spent_time:
            self.local._bee_base_t1 = datetime.now()
    
    def doBeforeReturn(self, list_param:list):
        self.__spent_time()
        pass
        
    def doBeforeReturnSimple(self):
        self.__spent_time()
        pass
            
    def __spent_time(self):
        show_sql_spent_time = False #TODO config
        if not show_sql_spent_time:
            return
        
        #子类在调用此方法时，记录当前的时间，p_t2
        #并获取在doBeforePasreEntity时记录的t1时间，然后计算(p_t2-p_t1)的时间，作为运行消耗的时间。
        if not hasattr(self.local, '_bee_base_t1'):  
            Logger.warn("Do not call doBeforeParseEntity, do not register the start time")
        else:  
            p_t1 = self.local._bee_base_t1  
            p_t2 = datetime.now()  
            # spent_time = (p_t2 - p_t1).total_seconds()*1000
            spent_time = int((p_t2 - p_t1).total_seconds() * 1000) 
            # spent_time = (p_t2 - p_t1).microseconds
            Logger.info(f"spent time: {spent_time} ms")
            del self.local._bee_base_t1
    
    
    # def doAfterCompleteSql(self, sql):
    #     pass
    
    def log_params(self, params):
        show_sql_params = True #TODO config
        if not show_sql_params:
            return
        Logger.logsql("params:", params)

