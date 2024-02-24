from flask import session
from functools import wraps
def check_logged_in(func) ->'func':
    @wraps(func)
    def wrapper(*args,**kwargs): # this is the function returned by the decorator check_logged_in, this function decorates the 'decorated' function
        #any calls to the decorated function are replaced by calls to this function
        if 'islogin' in session:
            return func(*args,**kwargs)
        return 'you are not logged in'
    
    return wrapper

