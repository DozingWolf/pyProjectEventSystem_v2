
class SelfErrorList(Exception):
    def __init__(self,code, message):
        super().__init__(self)
        self.message = message
        self.code = code
        self.args = (message,)
    def __str__(self) -> str:
        return ''.join([self.code,': ',self.message])
    
class EmpytParameterError(SelfErrorList):
    def __init__(self, message):
        super().__init__('4001', message)

class ServerError(SelfErrorList):
    def __init__(self, message):
        super().__init__('4002', message)