from bee.osql.const import StrConst


class Version:
    '''
    Bee Version.
    '''
    __version = "1.6.8"
    vid = 1006008

    @staticmethod
    def getVersion():
        return Version.__version

    @staticmethod
    def printversion():
        print("[INFO] ", StrConst.LOG_PREFIX, "Bee Version is: " + Version.__version)

