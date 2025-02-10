import json
import os

from bee.osql.const import SysConst
from bee.osql.logger import Logger


# from bee.key import Key
class PreConfig:
    
    # suggest set project root path for it
    config_folder_root_path = ""
    
    # value is:lower,upper
    sql_key_word_case = None
    
    sql_placeholder="?"


class HoneyConfig:
    
    dbName  =None 
    host    =None 
    user    =None 
    password=None 
    database=None 
    port    =None
    
    _loaded = False # 标记是否已加载配置
    
    __db_config_data=None
    
    __instance = None
    
    def __new__(cls):  
        if cls.__instance is None: 
            Logger.debug("HoneyConfig.__new__") 
            cls.__instance = super().__new__(cls)
            cls.__loadConfigInProperties(cls)
            cls.__loadConfigInJson(cls)
            if cls.port is not None:
                cls.port=int(cls.port)  
        
        if cls.__db_config_data is None:
            Logger.info("Default loading and init configuration file failed!")
        return cls.__instance 
    
    @staticmethod
    def __adjust_config_file(cls, config_file):
        
        root_dir = PreConfig.config_folder_root_path
        
        # 构建两个可能的路径  
        resources_path = os.path.join(root_dir, 'resources', config_file)  # resources 目录下
        default_path = os.path.join(root_dir, config_file)  # 工程根目录下  
        
        try:
            # 优先加载 resources 目录中的文件  
            if os.path.exists(resources_path): 
                config_file = resources_path  
            elif os.path.exists(default_path): 
                config_file = default_path 
        except OSError as err: 
            Logger.error(err)
            # raise ConfigBeeException(err)
        return config_file

    @staticmethod
    def __loadConfigInProperties(cls):
        if cls._loaded:
            return 
        config_file = SysConst.configPropertiesFileName  # 文件路径 
        
        try:
            config_file = cls.__adjust_config_file(cls, config_file)
            with open(config_file, 'r') as file:
                cls._loaded = True  # 设置为已加载   
                Logger.info("Loading config file: " + config_file)
                for line in file: 
                    line = line.strip() 
                    # 跳过空行和注释 
                    if not line or line.startswith('#'): 
                        continue 
                    # 拆分键值对
                    try: 
                        key, value = line.split('=', 1)  
                        key = key.strip()  
                        value = value.strip()
                    except ValueError as err: 
                        Logger.error(err, line)
                        continue  
        
                    # 检查键是否以 'bee.db.' 开头 
                    if key.startswith('bee.db.'): 
                        # 获取属性名称 
                        attr_name = key[len('bee.db.'):]  
                        # 将值赋给对应的属性
                        if hasattr(cls, attr_name): 
                            setattr(cls, attr_name, value)
                        
            cls.__db_config_data = cls.__instance.get_db_config_dict()            
        except OSError as err: 
            Logger.info(err)
            # raise ConfigBeeException(err)
                        
    @staticmethod 
    def __loadConfigInJson(cls): 
        if cls._loaded:
            return
         
        config_file = SysConst.configJsonFileName
        
        try:
            config_file = cls.__adjust_config_file(cls, config_file)
            Logger.info("Loading config file: "+config_file)
            with open(config_file, 'r') as file: 
                cls._loaded = True  # 设置为已加载                      
                cls.__db_config_data = json.load(file) 
                
                cls.dbName = cls.__db_config_data.get("dbName")
                
        except OSError as err: 
            Logger.error(err)
                        
    def get_db_config_dict(self):  
        """将DB相关的类属性打包成字典并返回""" 
        cls=type(self)
        if cls.__db_config_data is not None:
            return cls.__db_config_data
        
        cls.__db_config_data={}
        
        if HoneyConfig.dbName is not None:  
            cls.__db_config_data['dbName'] = HoneyConfig.dbName
        if HoneyConfig.host is not None:  
            cls.__db_config_data['host'] = HoneyConfig.host
        if HoneyConfig.user is not None:  
            cls.__db_config_data['user'] = HoneyConfig.user
        if HoneyConfig.password is not None:  
            cls.__db_config_data['password'] = HoneyConfig.password
        if HoneyConfig.database is not None:  
            cls.__db_config_data['database'] = HoneyConfig.database
        if HoneyConfig.port is not None:  
            cls.__db_config_data['port'] = int(HoneyConfig.port)
        
        return cls.__db_config_data
    
    def set_db_config_dict(self,config):
        cls=type(self)
        cls.__db_config_data=config
        
        if config is not None:
            Logger.info("Reset db_config_data")
        if config.get("dbName") is not None:
            if cls.__db_config_data is None:
                cls.__db_config_data={}
            cls.__db_config_data["dbName"] = config.get("dbName")   
           
    def get_dbName(self):
        return HoneyConfig.dbName.lower()
    
    def set_dbName(self, dbName):
        HoneyConfig.dbName = dbName

    
# if __name__ == '__main__':
#     print("start")
#     c1=HoneyConfig()
#     print(c1)
#     c2=HoneyConfig()
#     print(c2)
