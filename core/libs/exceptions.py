class SnyneError(Exception):

    status_code = 400
    message = 'error_message'

    def __init__(self,status_code,message):
        Exception.__init__(self)
        self.status_code=status_code
        self.message=message