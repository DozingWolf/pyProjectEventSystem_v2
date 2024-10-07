
class SelfErrorList(Exception):
    def __init__(self,code, message,keycolumn=None):
        super().__init__(self)
        self.message = message
        self.code = code
        self.args = (message,)
    def __str__(self) -> str:
        return ''.join([self.code,': ',self.message])

class NoneJsonKey(SelfErrorList):
    # Json传参没有相关的Key错误
    def __init__(self, message,keycolumn=None):
        super().__init__('4001', message)
        self.errorColumn = keycolumn
    def __str__(self) -> str:
        return ''.join([self.code,': ',self.message,', key:',self.errorColumn])

class EmptyJsonValue(SelfErrorList):
    # Json传参某Key没有必须的值错误（非空错误）
    def __init__(self, message,keycolumn):
        super().__init__('4002', message)
        self.errorColumn = keycolumn
    def __str__(self) -> str:
        return ''.join([self.code,': ',self.message,', key:',self.errorColumn])

class ErrorJsonData(SelfErrorList):
    # Json传参的值不合法错误
    def __init__(self, message,keycolumn=None,send=None):
        super().__init__('4003', message)
        self.errorColumn = keycolumn
        self.errorValue = send
    def __str__(self) -> str:
        return ''.join([self.code,': ',self.message,', key:',self.errorColumn,', value:',self.errorValue])