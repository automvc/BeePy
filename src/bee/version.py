from bee.osql.const import StrConst


class Version:
    __version = "1.5.4"
    vid=1005004
    
    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)
    
