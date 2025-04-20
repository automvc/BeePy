from bee.name.NameUtil import toCamelNaming, toUnderscoreNaming, \
    firstLetterToUpper
from bee.name.naming_handler import NamingHandler


if __name__=="__main__": 
    newName = NamingHandler.toColumnName("userName,className")
    print(newName)
    
    print(toCamelNaming("_aaa_bb_"))
    print(toCamelNaming("_aaa_bb"))

    print(toCamelNaming("user_name"))
    print(toCamelNaming("test_name"))
    name="testName"
    print(name.capitalize()) #bug 首字段大写，但还会把其它字母小写

    print(toUnderscoreNaming("userName"))
    print(toUnderscoreNaming("UserName"))

    print(firstLetterToUpper("testName"))