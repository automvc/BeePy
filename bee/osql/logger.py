from bee.osql.const import StrConst


class Logger:
    
    @staticmethod
    def debug(msg):
        print(StrConst.LOG_PREFIX+msg)
        
    @staticmethod
    def info(msg):
        print(StrConst.LOG_PREFIX+msg)

    @staticmethod
    def warn(msg):
        print(StrConst.LOG_PREFIX+msg)
        
    @staticmethod
    def error(msg):
        print(StrConst.LOG_PREFIX+msg)
        
    @staticmethod
    def logsql(*msg):
        # if msg is not None:
        #     msg[0]=StrConst.LOG_PREFIX+msg[0]
        if msg:  # 检查是否有传入参数  
            msg = (StrConst.LOG_SQL_PREFIX + msg[0],) + msg[1:]  # 添加前缀并保留其他参数  
        print(*msg)

