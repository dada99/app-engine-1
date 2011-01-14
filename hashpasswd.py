'''
Created on 2011-1-7

@author: liuda
'''
import os
from hashlib import sha256
import hashlib
from hmac import HMAC
 
def encrypt_password(password, salt=None):
    """Hash password on the fly."""
    if salt is None:
        salt = os.urandom(8) # 64 bits.
 
    assert 8 == len(salt)
    assert isinstance(salt, str)
 
    if isinstance(password, unicode):
        password = password.encode('UTF-8')
 
    assert isinstance(password, str)
 
    result = password
    original = password
    for i in xrange(10):
        result = HMAC(salt,result,sha256).digest()
        
    #result = hashlib.md5( password ).hexdigest()
    for i in xrange(10):
        original = HMAC(salt,original,sha256).digest()
    
    return result+"--------"+original
    #return result

if __name__ == "__main__": 
    a='123456'
    print encrypt_password(a)
    