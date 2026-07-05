from bee.osql.const import StrConst


class Version:
    '''
    Bee Version.
    '''
    __version = "1.9.0"
    vid = 1009000

    @staticmethod
    def getVersion():
        return Version.__version

    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)

