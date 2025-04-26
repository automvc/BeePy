from bee.osql.const import StrConst


class Version:
    __version = "1.6.0"
    vid = 1006000
    
    @staticmethod
    def getVersion():
        return Version.__version
    
    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)
        