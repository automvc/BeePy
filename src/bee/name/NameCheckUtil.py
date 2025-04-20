import re  
from bee.exception import BeeErrorNameException
from bee.osql.logger import Logger

# NameCheckUtil.py


def is_valid_name(name): 
    pattern = r'^[a-zA-Z]{1}[0-9a-zA-Z_.]*$'  
    return bool(re.match(pattern, name))  


def is_not_valid_name(name): 
    return not is_valid_name(name)  


def check_fields(name): 
    if name and ',' in name: 
        names = name.split(',')  
        for n in names: 
            _check_one_name(n.strip())  
    else: 
        _check_one_name(name)  

def _check_one_name(name):
    if not name: 
        raise BeeErrorNameException("The name is null.")  
    
    if name.lower() == "count(*)": 
        return  

    # Assuming it checks for keyword names.  
    if is_key_name(name): 
        Logger.warn(f"The name : '{name}' , it is key word name!")  

    if is_valid_name(name): 
        return  
    else: 
        if is_illegal(name): 
            raise BeeErrorNameException(f"The name: '{name}' is illegal!")  
        else: 
            Logger.debug(f"The name is '{name}' , does not conform to naming conventions!")   


def is_key_name(name): 
    # Placeholder for keyword checking. Implement as needed.  
    keyword_names = {"select", "from", "where", "insert", "update", "delete", "count(*)"}  
    return name.lower() in keyword_names  


def is_illegal(field_name): 
    if (not field_name or   
        ' ' in field_name or   
        '-' in field_name or   
        '#' in field_name or   
        '|' in field_name or   
        '+' in field_name or   
        '/*' in field_name or   
        ';' in field_name or   
        '//' in field_name): 
        return True  
    return False  
