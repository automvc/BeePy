from datetime import time, date, datetime
from typing import Annotated, List, Set, Dict, Tuple


# full.py
class TestName:
    id:int = None
    myName:str = None
    name2: Annotated[str, "length=100"]  # 声明字符串长度为 100  
    myPrice: float = None  
    createdAt: datetime  # 日期时间字段  
    updatedTime: time  # 日期字段  
    flag:bool = None
    set0:set = None
    map:dict = None
    list0:list = None
    list1:List = None
    remark = None
    tuple0:tuple = None
    descstr:str = None
    modifyDate: date
    updatedAt2: date
    
    set1:Set = None
    map1:Dict = None
    tuple1:Tuple = None
    
    setTwo:Set = None
    mapTwo:Dict = None
    tupleTwo:Tuple = None
    listTwo:List = None
    
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
    
