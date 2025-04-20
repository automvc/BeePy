import threading  
from typing import Dict, Any, Optional  


class OneTimeParameter: 
     
    __local = threading.local()  
    
    @staticmethod  
    def get_attribute(key: str) -> Optional[Any]: 
        if not hasattr(OneTimeParameter.__local, 'storage'): 
            return None  
        storage: Dict[str, Any] = OneTimeParameter.__local.storage  
        value = storage.pop(key, None)  # Remove after getting  
        return value  
    
    @staticmethod  
    def set_attribute(key: str, obj: Any) -> None: 
        if obj is None: 
            return  
        if not hasattr(OneTimeParameter.__local, 'storage'): 
            OneTimeParameter.__local.storage = {}  
        OneTimeParameter.__local.storage[key] = obj  
    
    @staticmethod  
    def set_true_for_key(key: str) -> None: 
        OneTimeParameter.set_attribute(key, "TRUE")  # Using string "TRUE" as equivalent  
    
    @staticmethod  
    def is_true(key: str) -> bool: 
        value = OneTimeParameter.get_attribute(key)  
        return value == "TRUE"  
    
    @staticmethod  
    def remove() -> None: 
        if hasattr(OneTimeParameter.__local, 'storage'): 
            del OneTimeParameter.__local.storage  
