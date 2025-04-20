
import re 

from bee.context import HoneyContext

from bee.osql.paging import Paging


# SqlUtil.py
def add_paging(sql, start, size):
    
    if (not start and start != 0) and not size:
        return sql
    
    if not start:
        start = 0
    
    if not size:
        size = 100  # todo get from config?
    
    paging = Paging()
    sql = paging.to_page_sql(sql, start, size)
    
    return sql


def transform_sql(sql, params_dict = None): 
    if not params_dict: 
        return sql
        # params_dict = {}  
    
    # 用于存储处理后的 SQL 查询和参数  
    para_array = [] 
    
    placeholder = HoneyContext.get_placeholder()  
    
    # 用正则表达式匹配所有类似 #{variable} 的模式  
    def replace_placeholder(match): 
        # 提取变量名  
        var_name = match.group(1)  
        # 将变量名添加到参数数组  
        para_array.append(var_name)  
        # return '?'   # bug  fixed V1.6.0
        return placeholder  
    
    # 使用正则替换查询中的变量  
    sql_transformed = re.sub(r'#\{(\w+)\}', replace_placeholder, sql)  
    
    # 从 params_dict 中获取参数值 
    params = [params_dict[var] for var in para_array]  
    
    return sql_transformed, params
