import re
from data import *

def token_check(token):
    return False

def check_email(email): 
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  
    if(re.search(regex,email)):  
        return True  
    else:
        return False