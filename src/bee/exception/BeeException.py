class BeeException(Exception):

    def __init__(self, message=None, code=None):
        super().__init__(message)
        self.code = code
        
    def __str__(self):
        if self.code is not None:  
            return f"{super().__str__()} (error code: {self.code})"
        return super().__str__()
