'''
Created on 2011-1-7

@author: liuda
'''
import os
import Cookie
from google.appengine.ext import db

from appengine_utilities.sessions import Session
from hashlib import md5

class Myuser(db.Model):
    COOKIE_NAME = 'mysite-cookie'
    name=db.StringProperty()
    passwd=db.StringProperty()
    signupdate=db.TextProperty() 
    cookieid=db.StringProperty()
    expiredate=db.DateProperty()
    
    def get_current_user(self):
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        cookie = Cookie.SimpleCookie()
        cookie.load(string_cookie)
        try:
            cookie[self.COOKIE_NAME]
            return 'You have log in!'
        except KeyError:
            return 'Please log in'
       
        
    def set_user_cookie(self,cookiename=COOKIE_NAME,expireperiod=None,username='user'):  
        #string_cookie = os.environ.get('HTTP_COOKIE', '')
        cookie = Cookie.SimpleCookie()
        
        cookiedata = md5(username).hexdigest()
        #rint cookiedata
        cookie[cookiename]=cookiedata
        return cookie
    
   
    
   
    
    
              
    
        