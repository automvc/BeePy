from bee.api import SuidRich
from bee.config import PreConfig
from entity.Orders_202501 import Orders_202501

# test unique,index_normal

if __name__ == '__main__':
    print("start")
    
    #suggest set project root path for it
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    suidRich = SuidRich()
    suidRich.create_table(Orders_202501,True)
    
    suidRich.unique(Orders_202501, "name")
    # suidRich.index_normal(Orders_202501, "name*")
    # suidRich.index_normal(Orders_202501, "name#")
    # suidRich.index_normal(Orders_202501, "name","name#")
    
    entity=Orders_202501()
    entity.name="2025"
    entity.remark="test create table"
    suidRich.insert(entity)
    suidRich.insert(entity)
    
    one = suidRich.select(Orders_202501())
    print(one)
    
    
