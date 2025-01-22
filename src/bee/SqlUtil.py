
import re 
from bee.paging import Paging

# SqlUtil.py


def add_paging(sql, start, size):
    
    if start is None and size is None:
        return sql
    
    if start is None:
        start = 0
    
    if size is None:
        size = 100  #TODO get from config
    
    paging = Paging()
    sql = paging.to_page_sql(sql, start, size)
    
    return sql

def transform_sql(sql, params_dict=None): 
    if params_dict is None: 
        return sql
        # params_dict = {}  
    
    # 用于存储处理后的 SQL 查询和参数  
    para_array = []  
    
    # 用正则表达式匹配所有类似 #{variable} 的模式  
    def replace_placeholder(match):  
        # 提取变量名  
        var_name = match.group(1)  
        # 将变量名添加到参数数组  
        para_array.append(var_name)  
        return '?'  
    
    # 使用正则替换查询中的变量  
    sql_transformed = re.sub(r'#\{(\w+)\}', replace_placeholder, sql)  
    
    # 从 params_dict 中获取参数值，生成参数元组  
    params_tuple = tuple(params_dict[var] for var in para_array)  
    
    # 这里可以执行 SQL 查询、返回结果等  
    # print(sql_transformed, params_tuple)  # Debug output  
    # 假设你实现了数据库查询逻辑，可以在此处添加更多代码。  
    
    return sql_transformed, params_tuple
