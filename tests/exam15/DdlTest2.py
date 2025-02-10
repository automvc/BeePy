from bee.api import SuidRich
from bee.config import PreConfig
from entity.Orders_2025 import Orders_2025


if __name__ == '__main__':
    print("start")
    
    #suggest set project root path for it
    PreConfig.config_folder_root_path="E:\\JavaWeb\\eclipse-workspace202312\\BeePy-automvc\\tests\\exam"
    
    suidRich = SuidRich()
    suidRich.create_table(Orders_2025)
    
    # one = suidRich.select(Orders_2025)
    # print(one)
    
    
