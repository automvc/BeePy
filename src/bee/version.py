from bee.osql.const import StrConst


class Version:
    __version = "1.5.0"
    vid=1005000
    
    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)
    
