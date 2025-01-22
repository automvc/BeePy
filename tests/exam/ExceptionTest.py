# from bee.exception.BeeException import BeeException
# from bee.exception.ConfigBeeException import ConfigBeeException
from bee.exception import BeeException, ConfigBeeException


# from bee.exception.ConfigBeeException import ConfigBeeException
# from bee.exception.ConfigBeeException import ConfigBeeException
if __name__ == "__main__":
    print("start...")
    try:
        # raise BeeException("--BeeException--")
        # raise BeeException("--BeeException--",500)
        raise BeeException()
    except BeeException as e:
        print("define exception : ", e)
        
    try:
        # raise ConfigBeeException()
        raise ConfigBeeException("--ConfigBeeException--",500)
    except ConfigBeeException as e:
        print("define exception : ", e)
