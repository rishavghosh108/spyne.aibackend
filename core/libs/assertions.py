from .exceptions import SnyneError

def base_error(error_code,msg):
    raise SnyneError(status_code=error_code,message=msg)

def assert_valid(status,msg='BAD_REQUEST'):
    if status is False:
        base_error(400,msg)

def assert_found(_obj, msg='NOT_FOUND'):
    if _obj is None:
        base_error(404,msg)