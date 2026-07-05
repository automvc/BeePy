class BeeException(Exception):
    '''
    BeeException is Bee framework Base Exception.
    '''

    def __init__(self, message_or_exception = None, code = None):
        super().__init__(message_or_exception)
        self.code = code

    def __str__(self):
        if self.code:
            return f"{super().__str__()} (error code: {self.code})"
        return super().__str__()


class ConfigBeeException(BeeException):
    pass


class SqlBeeException(BeeException):
    pass


class ParamBeeException(BeeException):
    pass


class BeeErrorNameException(BeeException):
    pass


class BeeErrorGrammarException(BeeException):
    pass
