from bee.api import SuidRich
from bee.config import PreConfig
from entity.Orders_202501 import Orders_202501


if __name__ == '__main__':
    print("start")
    
    #suggest set project root path for it
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    suidRich = SuidRich()
    # suidRich.create_table(Orders_202501)
    suidRich.create_table(Orders_202501,True)
    
    # entity=Orders_202501()
    # entity.name="2025"
    # entity.remark="test create table"
    # suidRich.insert(entity)
    
    one = suidRich.select(Orders_202501())
    print(one)
    
    
