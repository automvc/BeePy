from datetime import time, date, datetime
# from typing import Annotated, List, Set, Dict, Tuple
from typing import List, Set, Dict, Tuple

from bee.typing import String


# full.py
class Entity:
    id:int = None
    name:str = None
    # name2: Annotated[str, "length = 100"]  # 声明字符串长度为 100  
    # name3: Annotated[str, "len = 100"]  # 声明字符串长度为 100  length or len
    name4:String(99)
    name5:String
    price: float = None  
    created_at: datetime  # 日期时间字段  
    updated_time: time  # 日期字段  
    flag:bool = None
    set0:set = None
    map:dict = None
    list0:list = None
    list1:List = None
    remark = None
    tuple0:tuple = None
    descstr:str = None
    modify_date: date
    updated_at2: date
    
    set1:Set = None
    map1:Dict = None
    tuple1:Tuple = None
    
    ttt:bytes=None
    
    # n:Number= None
    # id3:Int = None
    # name3:String = None
    # flag3:BOOLEAN = None
    
    # 无声明类型与复合类型邻近，则无法识别；默认先处理复合类型
    # descstr=None
    # modify_date: date
    # updated_at2: date
    # 结果变为：
    # modify_date DATE,
    # updated_at2 DATE,
    # descstr VARCHAR(255)
    
    def __repr__(self): 
        return  str(self.__dict__) 
    
