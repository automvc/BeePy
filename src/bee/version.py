from bee.osql.const import StrConst


class Version:
    __version = "1.6.2"
    vid = 1006002
    
    @staticmethod
    def getVersion():
        return Version.__version
    
    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)

