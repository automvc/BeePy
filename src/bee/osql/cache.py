import array   
import copy
import threading
from typing import Any, Dict, List, Set

from bee.config import HoneyConfig
from bee.context import HoneyContext
from bee.osql import Util
from bee.osql.logger import Logger

from bee.osql.bee_enum import LocalType
from bee.osql.index import CacheArrayIndex


class CacheUtil: 
    
    # 一般缓存  
    __map: Dict[str, int] = {}  # <key, index>  
    __obj = None  # 存放缓存对象  
    __keys = None  # 保存key的数组  
    __time = None  # 存放当前毫秒的时间数组
    
    __table_indexSet_map: Dict[str, Set] = {}  # e.g. {"table_name": {1,2,5} }     {'table_name': {indexSet})
    __key_tableNameList_map: Dict[str, List] = {}  # e.g. {"key": ['table1','table2']

    # 特殊缓存  
    _set1: Set[str] = set()  # 从不放缓存的表名集合  
    _set2: Set[str] = set()  # 永久放缓存的表名集合  //改成外部不可访问
    _set3: Set[str] = set()  # 长久放缓存的表名集合  

    __map2: Dict[str, Any] = {}  # 永久缓存  
    __map3: Dict[str, Any] = {}  # 长久缓存 (有修改时，会删除缓存，下次再获取就会是新的)  

    __set2_exist: Set[str] = set()  # 已放入永久缓存的key集合  
    __set3_exist: Set[str] = set()  # 已放入长久缓存的key集合 
    __map3_table_keySet: Dict[str, Set] = {} 

    __lock = threading.Lock()  # 用于线程安全
    __cache_init = False 
    __MAX_SIZE = None
    # __cacheArrayIndex = CacheArrayIndex() #不可以在属性就new,否则import SuidRich时，就会运行CacheArrayIndex的__init__方法
    __cacheArrayIndex = None
    
    @classmethod  
    def __init0(cls): 
        if not cls.__cache_init: 
            with cls.__lock: 
                if not cls.__cache_init:
                    _init_Max_Size = HoneyConfig.cache_max_size
                    cls.__MAX_SIZE = _init_Max_Size
                    cls.__keys = Array(_init_Max_Size)
                    cls.__time = LongArray(_init_Max_Size)
                    cls.__obj = Array(_init_Max_Size)
                    
                    cls.__cacheArrayIndex = CacheArrayIndex()
                    
                    cls.__cache_init = True
    
    # 不允许被继承                
    def __init_subclass__(self): 
        raise TypeError("CacheUtil cannot be subclassed")   

    @staticmethod  
    def __get_table_name(sql: str) -> str: 
        # todo 可能有多个table 用逗号分隔？？
        
        cacheSuidStruct = HoneyContext.get_data(LocalType.CacheSuidStruct, sql)
        if cacheSuidStruct:
            return cacheSuidStruct.tableNames
        else: 
            return None
    
    @staticmethod  
    def __genKey(sql: str) -> str: 
        
        cacheSuidStruct = HoneyContext.get_data(LocalType.CacheSuidStruct, sql)
        k = None
        if cacheSuidStruct:
            msg = f"{sql} # {str(cacheSuidStruct.params)} # {cacheSuidStruct.returnType} # {str(cacheSuidStruct.entityClass)} # {cacheSuidStruct.suidType.get_name()}"
            k = msg
        else:
            k = sql
        
        if HoneyConfig.cache_key_use_md5 == True:
            return Util.string_to_md5(k)
        else:
            return k
        
    @staticmethod  
    def add(sql: str, rs: Any):
        
        CacheUtil.__init0() 
        
        key = CacheUtil.__genKey(sql)
        table_name = CacheUtil.__get_table_name(sql)  

        # 1. 检查是否在set1（从不缓存）  
        if table_name in CacheUtil._set1: 
            return False

        # 2. 检查是否在set2（永久缓存）  
        if table_name in CacheUtil._set2: 
            if key not in CacheUtil.__set2_exist: 
                CacheUtil.__set2_exist.add(key)  
                CacheUtil.__map2[key] = rs  
            return True

        # 3. 检查是否在set3（长久缓存）  
        if table_name in CacheUtil._set3: 
            if key not in CacheUtil.__set3_exist: 
                CacheUtil.__set3_exist.add(key)  
                CacheUtil.__map3[key] = rs
                
                CacheUtil.__reg_map3_table_keySet(table_name, key)
            return True
        
        if(CacheUtil.__cacheArrayIndex.is_would_be_full()):
            if HoneyConfig.show_sql:
                Logger.info(" Cache would be full!")
            
            # 快满了,删除一定比例最先存入的
            CacheUtil._del_cache_in_between(CacheUtil.__cacheArrayIndex.get_delete_cache_index())
            # 上一句改为新线程运行才启用 todo
            # if CacheUtil.__cacheArrayIndex.get_used_rate() >= 90:
            #  if HoneyConfig.show_sql:
            #     Logger.warn("[Bee] ==========Cache already used more than 90% !");
            #     return False  # 快满了,本次不放缓存,直接返回

        # 4. 一般缓存  
        with CacheUtil.__lock: 
            index = CacheUtil.__cacheArrayIndex.get_next()
            
            CacheUtil.__map[key] = index  
            CacheUtil.__obj[index] = rs
            CacheUtil.__keys[index] = key 
            CacheUtil.__time[index] = Util.currentMilliseconds()
            
            CacheUtil.__key_tableNameList_map[key] = table_name
            
            CacheUtil.__reg_table_indexSet_map(table_name, index)
            
            return True
        
        return False
    
    # reg index set to table_dict    table关联它相关的缓存的下标。 
    @staticmethod  
    def  __reg_table_indexSet_map(table_name:str, index:int): 
        indexSet = CacheUtil.__table_indexSet_map.get(table_name, None)
        if indexSet:
            indexSet.add(index)
        else:
            indexSet = set()
            indexSet.add(index) 
            CacheUtil.__table_indexSet_map[table_name] = indexSet
        
    @staticmethod  
    def  __reg_map3_table_keySet(table_name:str, key:int): 
        keySet = CacheUtil.__map3_table_keySet.get(table_name, None)
        if keySet:
            keySet.add(key)
        else:
            keySet = set()
            keySet.add(key) 
            CacheUtil.__map3_table_keySet[table_name] = keySet

    @staticmethod  
    def get(sql: str) -> Any:
        
        CacheUtil.__init0() 
        
        key = CacheUtil.__genKey(sql)
         
        index = CacheUtil.__map.get(key, None)    
        if index == 0 or index: 
            if CacheUtil.__is_timeout(index):
                if CacheUtil.__cacheArrayIndex.is_start_delete():
                    # 删除多个  todo 起一个线程
                    CacheUtil._del_cache_in_between(index)
                else:
                    CacheUtil.__del_one_cache(index) 

                return None
            return copy.deepcopy(CacheUtil.__obj[index])  # 返回深拷贝  

        # 检查永久缓存  
        if key in CacheUtil.__set2_exist: 
            return copy.deepcopy(CacheUtil.__map2.get(key))  # 返回深拷贝  

        # 检查长久缓存  
        if key in CacheUtil.__set3_exist: 
            return copy.deepcopy(CacheUtil.__map3.get(key))  # 返回深拷贝  

        return None
    
    @staticmethod  
    def __is_timeout(index: int) -> bool: 
        timeout = HoneyConfig.cache_timeout  # 缓存过期时间,以毫秒为单位
        return  Util.currentMilliseconds() - CacheUtil.__time[index] >= timeout  
    
    @staticmethod  
    def __del_one_cache(index: int):
        Logger.debug("del one cache, index is: " + str(index))
        key = CacheUtil.__keys[index]
        CacheUtil.__del_one_index(key, index)
              
        CacheUtil.__del_one_normal_cache(index)
    
    @staticmethod  
    def __del_one_normal_cache(index: int):
        with CacheUtil.__lock: 
            key = CacheUtil.__keys[index]  
            if key in CacheUtil.__map: 
                del CacheUtil.__map[key]  
                CacheUtil.__time[index] = 0  
                CacheUtil.__obj[index] = None  
                CacheUtil.__keys[index] = None
                
    @staticmethod  
    # _del_one_index in tableIndexSet
    def __del_one_index(key: str, index: int): 
        # 这里可以添加维护表相关索引的逻辑  
        
        table_name = CacheUtil.__key_tableNameList_map[key]
        indexSet = CacheUtil.__table_indexSet_map.get(table_name, None)
        if indexSet:
            indexSet.remove(index)  # test

    @staticmethod  
    def clear(sql: str):
        CacheUtil.__init0()
        
        table_name = CacheUtil.__get_table_name(sql)
        indexSet = CacheUtil.__table_indexSet_map.pop(table_name, None)
        if indexSet:
            for index in indexSet:
                CacheUtil.__del_one_normal_cache(index)
        else:  # __map3
            keySet = CacheUtil.__map3_table_keySet.pop(table_name, None)
            if keySet:
                for key in keySet:
                    del CacheUtil.__map3[key]
                    
    @staticmethod                
    def _del_cache_in_between(know_index: int): 
        """  
        删除 low 和 know 之间的缓存（包含两端）  
        :param know_index: 已知超时的索引位置  
        """  
        max_size = CacheUtil.__MAX_SIZE
        array_index = CacheUtil.__cacheArrayIndex
        
        low = array_index.low  
        high = array_index.high  
        know = know_index  
    
        def _delete_cache_by_index(i: int): 
            CacheUtil.__del_one_cache(i)

        if low <= high: 
            # 情况1：正常顺序（low <= high）  
            for i in range(low, know + 1):  # 包含 know  
                _delete_cache_by_index(i)  
            CacheUtil.__cacheArrayIndex.low = (know + 1) % max_size  # 处理循环
            
            msg = f"delete cache from {low} to {know}, new low: {CacheUtil.__cacheArrayIndex.low}"
            Logger.debug(msg)  
        else: 
            # 情况2：循环缓存（low > high）  //all:0-99;  low 80    know:90   99, 0  20:high
            if low < know: 
                # 子情况2.1：know 在 low 之后（未跨循环点）  
                for i in range(low, know + 1): 
                    _delete_cache_by_index(i)  
                CacheUtil.__cacheArrayIndex.low = (know + 1) % max_size
                
                msg = f"delete cache from {low} to {know}, new low: {CacheUtil.__cacheArrayIndex.low}"
                Logger.debug(msg)
                   
            elif know < high:  # all:0-99; low 80    90   99, 0   know:10  20:high
                # 子情况2.2：know 在 high 之前（跨循环点）  
                # 删除从 low 到末尾的部分  
                for i in range(low, max_size): 
                    _delete_cache_by_index(i)  
                # 删除从开头到 know 的部分  
                for i in range(0, know + 1): 
                    _delete_cache_by_index(i)
                CacheUtil.__cacheArrayIndex.low = know + 1  # 自动处理循环（因为 know < high < low）
                
                CacheUtil.__cacheArrayIndex.low = (know + 1) % max_size
                msg = f"delete cache from {low} to {max_size},{know}, new low: {CacheUtil.__cacheArrayIndex.low}"  
                    
    # @staticmethod  
    # def _getMap():  # TEST for test todo
    #     print("cache map size: ", len(CacheUtil.__map))
    #     return CacheUtil.__map

    
class Array:
    
    __array:None
    __size = 0
    
    def __init__(self, size:int):
        self.__size = size
        self.__array = [None] * size
    
    def __setitem__(self, index:int, v:str):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return
        self.__array[index] = v
     
    def __getitem__(self, index):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return None
        return self.__array[index] 
    
    def __str__(self):
        # print(type(self.__array))   #<class 'list'>
        return "array len:" + str(len(self.__array)) + ", value:" + str(self.__array)
    

class LongArray:
    
    __array:None
    __size = 0
    
    def __init__(self, size:int):
        self.__size = size
        self.__array = array.array("Q", [0] * size)
    
    def __setitem__(self, index:int, v):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return
        self.__array[index] = v
     
    def __getitem__(self, index):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return None
        return self.__array[index] 
    
    def __str__(self):
        return "array len:" + str(len(self.__array)) + ", value:" + str(self.__array)
    
# if __name__ == '__main__':
#     print("start")
#     sa = Array(10)
#     sa[5] = "abc"
#
#     print(sa)
#     print(type(sa))
#
#     long_array = LongArray(10)
#     long_array[6] = 6
#     long_array[10] = 10 # test: Error index: 10
#     print(long_array)
#
#     # print(K.__sql_keywords)
#
# if __name__ == "__main__":
#     # 示例：使用 CacheUtil 管理缓存，并验证深拷贝  
#     # 假设有以下 SQL 查询和结果  
#     sql1 = "SELECT * FROM users WHERE id = 1"  
#     result1 = {"id": 1, "name": "Alice"} 
#
#     print(result1) 
#
#     # 1. 添加一般缓存  
#     CacheUtil.add(sql1, result1)  
#     print("Added general cache for sql1")  
#
#     # 2. 获取一般缓存并修改  
#     cached_result1 = CacheUtil.get(sql1)
#     print("修改前", cached_result1)   
#     cached_result1["name"] = "Bob"  # 修改获取的缓存结果  
#     print("Modified cached result for sql1:", cached_result1)  
#
#     # 3. 再次获取缓存，验证是否被修改  
#     original_cached_result1 = CacheUtil.get(sql1)
#     print("再次获取，修改前", original_cached_result1)     
#     print("Original cached result for sql1:", original_cached_result1)  
#
#     sql1 = "SELECT * FROM orders WHERE id = 1"  # orders
#     result1 = {"id": 10, "name": "milk"} 
#     # 4. 添加永久缓存  
#     CacheUtil._set2.add("orders")  # 将 'orders' 表标记为永久缓存  
#     # CacheUtil._set2.add("users")  # 将 'orders' 表标记为永久缓存  
#     CacheUtil.add(sql1, result1)  # 再次添加 sql1，这次会放入永久缓存  
#     print("Added permanent cache for sql1")  
#
#     # 5. 获取永久缓存并修改  
#     cached_result1_permanent = CacheUtil.get(sql1)  
#     cached_result1_permanent["name"] = "apple"  # 修改获取的缓存结果  
#     print("Modified permanent cached result for sql1:", cached_result1_permanent)  
#
#     # 6. 再次获取永久缓存，验证是否被修改  
#     original_cached_result1_permanent = CacheUtil.get(sql1)  
#     print("Original permanent cached result for sql1:", original_cached_result1_permanent)
