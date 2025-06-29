class BeeException(Exception):
    
    def __init__(self, message_or_exception = None, code = None):
        super().__init__(message_or_exception)
        self.code = code
        
    def __str__(self):
        if self.code:
            return f"{super().__str__()} (error code: {self.code})"
        return super().__str__()


class ConfigBeeException(BeeException): ...


class SqlBeeException(BeeException): ...


class ParamBeeException(BeeException): ...


class BeeErrorNameException(BeeException): ...


class BeeErrorGrammarException(BeeException): ...
