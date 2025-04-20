from bee.name.naming_handler import NamingHandler

if __name__=="__main__": 
    newName = NamingHandler.toColumnName("userName,className")
    print(newName)