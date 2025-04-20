class BeeException(Exception):

    # def __init__(self, message=None, code=None):
    #     super().__init__(message)
    #     self.code = code
    
    # def __init__(self, message_or_exception=None, code=None):  
       
        # self.code = code
        # if isinstance(message_or_exception, Exception):  
        #     print("-------BeeException---Exception-------")
        #     # 如果参数是异常，则使用该异常的消息  
        #     super().__init__(str(message_or_exception))  
        #     # self.original_exception = message_or_exception  
        # elif isinstance(message_or_exception, str): 
        #     print("-------BeeException---str-------") 
        #     # 如果参数是字符串，则使用用户提供的消息  
        #     super().__init__(message_or_exception)  
        #     # self.original_exception = None  # 或者可以选择设置为 None  
        # else:  
        #     # 如果没有提供参数，使用默认消息  
        #     super().__init__("BeeException.")  
        #     # self.original_exception = None  

    # def __str__(self):  
    #     original_message = f" (caused by: {self.original_exception})" if self.original_exception else ""  
    #     return f"BeeException occurred: {super().__str__()}{original_message}"  
        
    # def __str__(self):
    #     if self.code is not None: 
    #         return f"{super().__str__()} (error code: {self.code})"
    #     return super().__str__()
    
    def __init__(self, message_or_exception=None, code=None):
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
