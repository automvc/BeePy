# NameUtil.py


def getClassName(obj): 
    return obj.__class__.__name__  


def toUnderscoreNaming(name): 
    if not name:
        return name
    result = []  
    for i, char in enumerate(name): 
        if char.isupper() and i != 0: 
            result.append('_')  
        result.append(char.lower())  
    return ''.join(result)  


def toCamelNaming(name): 
    if not name:
        return name
    name = name.strip()
    parts = name.split('_')
    if  len(parts[0]) == 0:
        parts = parts[1:]
    # print(parts)
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])  


def firstLetterToUpper(name): 
    if not name: 
        return name  
    return name[0].upper() + name[1:]
    #bug testName->Testname
    # return name.capitalize()


def firstLetterToLower(name): 
    if not name: 
        return name  
    return name[0].lower() + name[1:]  

# if __name__=="__main__":
# #
# #     print(toCamelNaming("_aaa_bb_"))
# #     print(toCamelNaming("_aaa_bb"))
# #
#     print(toCamelNaming("user_name"))
#     print(toCamelNaming("test_name"))
#     name="testName"
#     print(name.capitalize())
# #
# #     print(toUnderscoreNaming("userName"))
# #     print(toUnderscoreNaming("UserName"))
# #
#     print(firstLetterToUpper("testName"))

