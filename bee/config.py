import json

from bee.key import Key
from bee.osql.logger import Logger


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
    def __loadConfigInProperties(cls):
        if cls._loaded:
            return 
        config_file = Key.configPropertiesFileName # 文件路径 
        
        try:
            with open(config_file, 'r') as file:
                cls._loaded = True # 设置为已加载   
                print("Loading config file: "+config_file)
                for line in file:  
                    line = line.strip() 
                    # 跳过空行和注释 
                    if not line or line.startswith('#'):  
                        continue 
                    # 拆分键值对
                    try: 
                        key, value = line.split('=',1)  
                        key = key.strip()  
                        value = value.strip()
                    except ValueError as err: 
                        print(err,line)
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
            print(err)                   
                        
                        
    @staticmethod 
    def __loadConfigInJson(cls):  
        if not cls._loaded: #只加载一次 
            # config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')  
            config_file=Key.configJsonFileName
            print("Loading config file: "+config_file)
            try:
                with open(config_file, 'r') as config_file:  
                    cls._loaded = True # 设置为已加载                      
                    cls.__db_config_data = json.load(config_file) 
                    
                    cls.dbName=cls.__db_config_data.get("dbName")
                    
            except OSError as err: 
                print(err)   
                        
                        
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
        print("---------------:"+dbName)
        HoneyConfig.dbName = dbName
    
