from bee.osql.const import StrConst


class Logger:
    
    @staticmethod
    def debug(msg):
        print("[DEBUG] ",StrConst.LOG_PREFIX, msg)
        
    @staticmethod
    def info(msg):
        print("[INFO] ",StrConst.LOG_PREFIX, msg)

    @staticmethod
    def warn(msg):
        # print("[WARN] ",StrConst.LOG_PREFIX, msg)
        print("\033[31m[WARN]  " + StrConst.LOG_PREFIX + msg + "\033[0m ")
        
    @staticmethod
    def error(msg):
        # print("[ERROR] ",StrConst.LOG_PREFIX, msg)
        print("\033[31m[ERROR] " + StrConst.LOG_PREFIX + msg + "\033[0m ")
        
    @staticmethod
    def logsql(*msg):
        if msg:  # 检查是否有传入参数  
            msg = ("[INFO]  "+StrConst.LOG_SQL_PREFIX + msg[0],) + msg[1:]  # 添加前缀并保留其他参数  
        print(*msg)

