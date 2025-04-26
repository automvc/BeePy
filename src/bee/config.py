import json
import os

from bee.version import Version
from bee.exception import ConfigBeeException
from bee.osql.const import DatabaseConst
from bee.osql.logger import Logger


class PreConfig:
    
    # suggest set project root path for it
    config_folder_root_path = None  # replace with config_path since 1.6.0
    config_path = ""
    
    config_properties_file_name = "bee.properties"
    config_json_file_name = "bee.json"
    

class HoneyConfig:
    
    dbname = None 
    host = None 
    user = None 
    password = None 
    database = None 
    port:int = None
    
    # value is:lower,upper
    sql_key_word_case = "lower"
    sql_placeholder = "?"
    
    show_sql:bool = True
    show_sql_params:bool = True
    show_sql_spent_time:bool = False
    show_sql_spent_time_min_ms:int = 0
    
    #     (DB<-->Python),
    # 1: order_no<-->orderNo 
    # 2: ORDER_NO<-->orderNo
    # 3: original,
    # 4: ORDER_NO<-->order_no (DbUpperAndPythonLower)
    naming_translate_type:int = 3
    naming_to_lower_before:bool = True
    
    # cache的要提前用,不能设置为None.   是可以的，之前是因为Cache在属性使用了__cacheArrayIndex = CacheArrayIndex()引起；import时就会运行到。
    cache_max_size:int = 20000
    cache_start_delete_rate:float = 0.6  
    cache_full_used_rate:float = 0.9
    cache_full_clear_rate:float = 0.2
    cache_timeout:int = 10000
    
    cache_key_use_md5:bool = True
    
    # >= this-value will do not put in cache
    cache_donot_put_cache_result_min_size:int = 200
    
    _loaded = False  # 标记是否已加载配置
    __db_config_data = None
    __instance = None
    
    # 将 PreConfig 作为参数，传入。
    def __new__(cls): 
        if cls.__instance is None: 
            # Logger.debug("HoneyConfig.__new__") 
            Version.printversion()
            Logger.info("HoneyConfig instance...") 
            cls.__instance = super().__new__(cls)
            cls.__loadConfigInProperties(cls)
            cls.__loadConfigInJson(cls)
            if cls.port:
                cls.port = int(cls.port)  
            if cls.__db_config_data is None:
                Logger.info("Default loading and init configuration file failed!")
        return cls.__instance 
    
    @staticmethod
    def __adjust_config_file(cls, config_file):
        
        root_dir0 = PreConfig.config_folder_root_path
        root_dir = PreConfig.config_path
        if not root_dir and root_dir0:
            root_dir = root_dir0
        
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
        config_file = PreConfig.config_properties_file_name  # 文件路径 
        old_config_file=config_file
        
        try:
            config_file = cls.__adjust_config_file(cls, config_file)
            if not os.path.isfile(config_file):
                Logger.info(f"Not found the file {old_config_file}!")
                return
            with open(config_file, 'r') as file:
                cls._loaded = True  # 设置为已加载   
                Logger.info("Loading config file: " + config_file)
                annotations = cls.__annotations__
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
                            
                    # 检查键是否以 'bee.' 开头 
                    elif key.startswith('bee.'): 
                        # 获取属性名称 
                        attr_name = key[len('bee.'):]  
                        # 将值赋给对应的属性
                        if hasattr(cls, attr_name): 
                            # setattr(cls, attr_name, value) # 数据是否要转换类型？ 要，在以下转换
                            
                            # 获取类型提示（Python 3.5+）  
                            type_hint = annotations.get(attr_name)  
                            init_value = getattr(cls, attr_name) 
                             
                            # print(" value:",init_value, "attr_name:",attr_name)
                            
                            if type_hint is not None:  # 优先使用类型注解  
                                target_type = type_hint
                                # print("target_type： ",target_type," value:",init_value)  
                            elif init_value is not None:  # 其次使用默认值的类型  
                                target_type = type(init_value)  
                            else:  # 既无注解也无默认值，保持原样  
                                target_type = None  
                                
                            # print("target_type： ",target_type," value:",init_value, "attr_name:",attr_name)
                            
                            # 在 Python 中，将字符串 'False' 转换为布尔型变量时，直接使用 bool() 函数会得到 True，因为非空字符串在 Python 中会被视为 True
                            
                            try:
                                converted_value = None  
                                # converted_value = value if target_type is None else target_type(value)
                                # print("converted_value: ",converted_value)
                                if  target_type is None:
                                    converted_value = value
                                elif type_hint is not None and type_hint is bool:
                                    converted_value = value.lower() == 'true'
                                elif type_hint is not None:
                                    converted_value = target_type(value)
                                elif target_type is bool:
                                    converted_value = value.lower() == 'true'
                                else: 
                                    converted_value = target_type(init_value)

                                # print("target_type： ",target_type," converted_value:",converted_value, "attr_name:",attr_name)                                
                                setattr(cls, attr_name, converted_value)
                            except (ValueError, TypeError) as e: 
                                raise ValueError(f"Can not transform {value} to {target_type} (attr_name: {attr_name})") from e  
                        
            cls.__db_config_data = cls.__instance.get_db_config_dict()            
        except OSError as err: 
            Logger.info(err)
            # raise ConfigBeeException(err)
            
    bool_map = {'True': True, 'False': False} 
                        
    @staticmethod 
    def __loadConfigInJson(cls): 
        if cls._loaded:
            return
         
        config_file = PreConfig.config_json_file_name
        old_config_file=config_file
        
        try:
            config_file = cls.__adjust_config_file(cls, config_file)
            
            if not os.path.isfile(config_file):
                Logger.warn(f"Not found the file {old_config_file}!")
                return
            
            Logger.info("Loading config file: " + config_file)
            with open(config_file, 'r') as file: 
                cls._loaded = True  # 设置为已加载                      
                cls.__db_config_data = json.load(file) 
                
                cls.dbname = cls.__db_config_data.get("dbname")
                
        except OSError as err: 
            Logger.info(err)
            
    def __adjust_db_path_for_sqllite(self):
        cls = type(self)
        t_dbName = cls.__db_config_data['dbname']
        if t_dbName.lower() == DatabaseConst.SQLite.lower():
            
            t_database = cls.__db_config_data['database']
            if os.path.isfile(t_database): 
                return
            
            path_separator = os.path.sep  
            if path_separator not in t_database: 
                root_dir = PreConfig.config_path
                newPath = root_dir + path_separator + t_database
                Logger.info("adjust the SQLite db file path to: " + newPath)
                if not os.path.isfile(newPath):
                    raise ConfigBeeException(f"File not found in current path or adjust path: {newPath}")
                cls.__db_config_data['database'] = newPath
                        
    def get_db_config_dict(self): 
        """将DB相关的类属性打包成字典并返回""" 
        cls = type(self)
        if cls.__db_config_data:
            # adjust db path
            self.__adjust_db_path_for_sqllite()
            return cls.__db_config_data
        
        cls.__db_config_data = {}
        
        if HoneyConfig.dbname: 
            cls.__db_config_data['dbname'] = HoneyConfig.dbname
        if HoneyConfig.host: 
            cls.__db_config_data['host'] = HoneyConfig.host
        if HoneyConfig.user: 
            cls.__db_config_data['user'] = HoneyConfig.user
        if HoneyConfig.password: 
            cls.__db_config_data['password'] = HoneyConfig.password
        if HoneyConfig.database: 
            cls.__db_config_data['database'] = HoneyConfig.database  # adjust db path
        if HoneyConfig.port: 
            cls.__db_config_data['port'] = int(HoneyConfig.port)
            
        self.__adjust_db_path_for_sqllite()        
        return cls.__db_config_data
    
    def set_db_config_dict(self, config):
        if not config:
            return
        Logger.info("Reset db_config_data")
        cls = type(self)
        if cls.__db_config_data:
                cls.__db_config_data = {}
        cls.__db_config_data = config
        
        if config.get("dbname"):
            cls.__db_config_data["dbname"] = config.get("dbname")
            HoneyConfig.dbName=config.get("dbname")
           
    def get_dbname(self):
        if HoneyConfig.dbname is None:
            return None
        
        return HoneyConfig.dbname.lower()
    
    def set_dbname(self, dbname):
        Logger.info("set database name:" + dbname)
        HoneyConfig.dbname = dbname
    
# if __name__ == '__main__':
#     print("start")
#     c1=HoneyConfig()
#     print(c1)
#     c2=HoneyConfig()
#     print(c2)
