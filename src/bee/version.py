from bee.osql.const import StrConst


class Version:
    __version = "1.5.2"
    vid=1005002
    
    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)
    
