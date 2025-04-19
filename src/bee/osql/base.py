from datetime import datetime 
import threading
from typing import Any

from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.osql.logger import Logger

from bee.osql.bee_enum import SuidType, LocalType
from bee.osql.cache import CacheUtil
from bee.osql.transform import ParamUtil


class AbstractCommOperate:
    
    def __init__(self): 
        # HoneyConfig() # how to call first time
        self.local = threading.local()  # 初始化线程本地存储  

    def doBeforePasreEntity(self, entity, SuidType:SuidType):
        # 子类在调用此方法时，记录当前的时间，_bee_base_t1
        self.__reg_start_spent_time()
            
    def doBeforePasreListEntity(self, entityArray, SuidType:SuidType):
        self.__reg_start_spent_time()
    
    def doBeforeReturn(self, list_param:list):
        self.__spent_time()
        self.__removeCacheSuidStruct()
        
    def doBeforeReturnSimple(self):
        self.__spent_time()
        self.__removeCacheSuidStruct()
    
    def __removeCacheSuidStruct(self):
        HoneyContext._remove_one_local_type(LocalType.CacheSuidStruct)
    
    def __reg_start_spent_time(self):
        if HoneyConfig.show_sql_spent_time:
            self.local._bee_base_t1 = datetime.now()
                
    def __spent_time(self):
        show_sql_spent_time = HoneyConfig.show_sql_spent_time
        if not show_sql_spent_time:
            return
        
        if not hasattr(self.local, '_bee_base_t1'): 
            Logger.warn("Do not call doBeforeParseEntity, do not register the start time")
        else: 
            p_t1 = self.local._bee_base_t1  
            p_t2 = datetime.now()  
            spent_time = int((p_t2 - p_t1).total_seconds() * 1000) 
            if spent_time > HoneyConfig.show_sql_spent_time_min_ms:
                Logger.info(f"spent time: {spent_time} ms")
            del self.local._bee_base_t1
    
    # def doAfterCompleteSql(self, sql):
    #     pass
    
    def logsql(self, hard_str, sql):
        if not HoneyConfig.show_sql:
            return
        Logger.logsql(hard_str, sql)
    
    def log_params(self, params):
        if not HoneyConfig.show_sql or not HoneyConfig.show_sql_params:
            return
        params = ParamUtil.transform_param(params)  # 1.6.0
        if params is None:
            return
        Logger.logsql("params:", params)
        
    def log_params_for_batch(self, params):
        if not HoneyConfig.show_sql_params:
            return
        # params=ParamUtil.transform_param(params) #1.6.0
        params = ParamUtil.transform_list_tuple_param(params)  # 1.6.0
        Logger.logsql("params:", params)
        

class AbstractBase:
    
    def addInCache(self, sql:str, rs:Any, resultSetSize:int):
        if resultSetSize >= HoneyConfig.cache_donot_put_cache_result_min_size:
            return
        CacheUtil.add(sql, rs)
        
    def loginfo(self, msg):
        if not HoneyConfig.show_sql:
            return
        Logger.info(msg)

