import threading  
from typing import Optional  

from bee.config import HoneyConfig


class CacheArrayIndex: 
    _instance_lock = threading.Lock()  
    _instance: Optional['CacheArrayIndex'] = None  

    def __new__(cls): 
        if cls._instance is None: 
            # print("--------CacheArrayIndex-----__new__-------")
            with cls._instance_lock: 
                if cls._instance is None: 
                    cls._instance = super().__new__(cls)  
                    # 初始化实例变量  
                    cls._instance._low = 0  # 低水位线（较旧的数据）  
                    cls._instance._high = 0  # 高水位线  
                    cls._instance._know = 0  # 已知超时点  
                    cls._instance._size = None
                    cls._instance._start_delete_cache_rate = 0.6  
                    cls._instance._full_used_rate = 0.9 
                    cls._instance._full_clear_cache_size = None
        return cls._instance  

    def __init__(self): 
        # 这些配置应该在首次使用时从配置加载
        if not hasattr(self, '_initialized'): 
            # print("--------CacheArrayIndex-----__init__-------")
            # # HoneyConfig()
            # print("--------CacheArrayIndex-----__init__-------,HoneyConfig.cache_start_delete_rate  :", HoneyConfig.cache_start_delete_rate)
            # print("--------CacheArrayIndex-----__init__-------,HoneyConfig.cache_full_used_rate  :", HoneyConfig.cache_full_used_rate)
            # print("--------CacheArrayIndex-----__init__-------,HoneyConfig.cache_max_size  :", HoneyConfig.cache_max_size)
            # print("--------CacheArrayIndex-----__init__-------,HoneyConfig._full_clear_cache_size  :", HoneyConfig.cache_full_clear_rate)
            
            self._start_delete_cache_rate = int(HoneyConfig.cache_start_delete_rate * 100)  
            self._full_used_rate = int(HoneyConfig.cache_full_used_rate * 100)  
            self._size = HoneyConfig.cache_max_size  
            self._full_clear_cache_size = int(HoneyConfig.cache_full_clear_rate * self._size)  
            self._lock = threading.RLock()  
            self._initialized = True  

    @property  
    def low(self) -> int: 
        with self._lock: 
            return self._low  

    @low.setter  
    def low(self, value: int): 
        with self._lock: 
            self._low = value  

    @property  
    def high(self) -> int: 
        return self._high  

    @property  
    def know(self) -> int: 
        return self._know  

    def get_used_size(self) -> int: 
        t = self.high - self.low  
        return t if t >= 0 else t + self._size  

    def get_empty_size(self) -> int: 
        return self._size - self.get_used_size()  

    def get_used_rate(self) -> int: 
        return (self.get_used_size() * 100) // self._size  

    def get_next(self) -> int: 
        with self._lock: 
            if self._high >= self._size: 
                self._high = 1  
                return 0  
            else: 
                result = self._high  
                self._high += 1  
                return result  

    def is_full(self) -> bool: 
        return self.get_empty_size() == 0  

    def is_would_be_full(self) -> bool: 
        return self.get_used_rate() >= self._full_used_rate  

    def get_delete_cache_index(self) -> int: 
        return (self.low + self._full_clear_cache_size - 1) % self._size  

    def is_start_delete(self) -> bool: 
        return self.get_used_rate() > self._start_delete_cache_rate  

# 使用示例  
# if __name__ == '__main__': 
#
#     # aa=HoneyConfig()
#
#     # 使用单例  
#     array_index = CacheArrayIndex()  
#     print(array_index.get_next())  # 线程安全的获取下一个索引  
#     print(array_index.get_next())  # 线程安全的获取下一个索引  
#
#     for i in range(22):
#         print(array_index.get_next()) 
    
