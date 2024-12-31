

class Logger:
    
    @staticmethod
    def debug(msg):
        print(msg)
        
    @staticmethod
    def info(msg):
        print(msg)

    @staticmethod
    def warn(msg):
        print(msg)
        
    @staticmethod
    def error(msg):
        print(msg)
        
    @staticmethod
    def logsql(*msg):
        print(*msg)

