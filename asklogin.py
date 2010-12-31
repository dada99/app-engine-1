# coding=utf-8
from google.appengine.api.urlfetch import DownloadError 
from appengine_utilities.sessions import Session
from appengine_utilities.sessions import _AppEngineUtilities_SessionData
from appengine_utilities.sessions import _AppEngineUtilities_Session
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson
import gdata.contacts.client
import oauth
import gdata.service
import gdata.contacts.service
import gdata.auth
import Cookie
import os
import pickle






CONSUMER_KEY = 'thedada99.appspot.com'
CONSUMER_SECRET = 'YSn7voZOD7XiEGIJdTCs6xbi'
SCOPES = ['https://docs.google.com/feeds/', 'https://www.google.com/calendar/feeds/']
SIG_METHOD = 'gdata.auth.OAuthSignatureMethod.HMAC_SHA1'
        #self.redirect('/')
client = gdata.contacts.service.ContactsService()

class GOauth1(webapp.RequestHandler): 
    def get(self):
        
        session = Session(cookie_name='google-oauth')
        
        if(self.request.get('oauth_token')==''):
            
            
            client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            req_token = client.FetchOAuthRequestToken()
            session['oauth_token_secret'] = req_token.secret
            client.SetOAuthToken(req_token)
            oauth_callback_url = self.request.uri
            
            
            self.redirect(client.GenerateOAuthAuthorizationURL(callback_url=oauth_callback_url))



        else:
            
            oauth_token = gdata.auth.OAuthTokenFromUrl(self.request.uri)
            
            if oauth_token:
                
                oauth_token.secret = session['oauth_token_secret']
                #print oauth_token.secret
                #oauth_token.oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                client.SetOAuthToken(oauth_token)
                #print client._oauth_input_params
                access_token = client.UpgradeToOAuthAccessToken()
                #session = Session(cookie_name='google-oauth',set_cookie_expires=False)
                session['access_token']=access_token
                
                #client.SetOAuthInputParameters(SIG_METHOD, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                #client1.SetOAuthToken(gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret))
                #oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1,CONSUMER_KEY, consumer_secret=CONSUMER_SECRET) 
                #oauth_token = gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret, oauth_input_params=oauth_input_params) 
                #client.SetOAuthToken(oauth_token) 
                #feed = client.GetDocumentListFeed()
                #for entry in feed.entry:
                    #print entry.title.text

                self.redirect('/')
                
            else:
                print 'No oauth_token found in the URL'  
                
                
class GOauth2(webapp.RequestHandler): 
    def get(self):
        
        res=db.GqlQuery("select * from _AppEngineUtilities_SessionData where keyname = 'access_token'")
        #client.RevokeOAuthToken()
        try:
            access_token=pickle.loads(res.fetch(1)[0].content)
        except IndexError:
            access_token=''
            self.response.out.write('There is NO valid token in the database.')
        if(access_token!=''):
            
             
            #client = gdata.contacts.client.ContactsClient() 
            client.SetOAuthInputParameters(SIG_METHOD, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            
            oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1,CONSUMER_KEY, consumer_secret=CONSUMER_SECRET) 
            oauth_token = gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret, oauth_input_params=oauth_input_params) 
            #client.SetOAuthToken(oauth_token)
            #out = gdata.service.lookup_scopes(client.service)
            #token = client.token_store.find_token(out[0])
            request_url='https://www.google.com/accounts/AuthSubRevokeToken'
            response = oauth_token.perform_request(client.http_client, 'GET', request_url,headers={'Content-Type':'application/x-www-form-urlencoded'})
            if(response.status==200):
                self.response.out.write(response.status)
                for i in _AppEngineUtilities_SessionData.all():
                    i.delete()
                    
                for i in _AppEngineUtilities_Session.all():
                    i.delete()
                
                
        

            
                       



        
class MainPage(webapp.RequestHandler):
    
    
    def get(self):
        

        #if user:
        self.response.out.write("""
            <head><meta name="google-site-verification" content="9vKkSHdgtRpI2oX1qN6Ne2QhL-ZVIqhl16NMpQLAIUo" /></head>
            """)
        self.response.out.write(
                'Please <a href="%s">Sign in</a>,for further process' % 
                users.create_login_url("/")
            )
        self.response.out.write('Go to <a href="/goauth">Google OAuth Sample</a><br />')
        self.response.out.write('Go to <a href="/goauth2">Google OAuth revoke</a><br />')
        
        #else:
        
        
        
        #access_token=_AppEngineUtilities_SessionData.gql("where id = 354")
        res=db.GqlQuery("select * from _AppEngineUtilities_SessionData where keyname = 'access_token'")
        try:
            access_token=pickle.loads(res.fetch(1)[0].content)
        except IndexError:
            access_token=''
            self.response.out.write('There is NO valid token in the database.')
        #self.response.out.write(access_token)
        if(access_token!=''):
            
            
            #client = gdata.contacts.client.ContactsClient() 
            client.SetOAuthInputParameters(SIG_METHOD, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            #client1.SetOAuthToken(gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret))
            oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1,CONSUMER_KEY, consumer_secret=CONSUMER_SECRET) 
            oauth_token = gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret, oauth_input_params=oauth_input_params) 
            client.SetOAuthToken(oauth_token) 
            #uri='http://www.google.com/m8/feeds/contacts/thedada99%40gmail.com/base/6d40d620f5958ca'
            #query = gdata.contacts.client.ContactsQuery()
            #query.max_results=300
            try:
                feed = client.GetContactsFeed()
            #feed = client.GetContactsFeed()
            
            #contact=feed.totalResults
                self.response.out.write(feed)
            except DownloadError:
                self.response.out.write('Download Fail,Pleae try again.')
                pass                
            
            #for i in feed:
             #   self.response.out.write(i)
              #  self.response.out.write('<br />')
               
            
            #for entry in feed:
                #self.response.out.write(entry+'<br/>') 
        
        
                    
            
#OAuth Consumer Key:     thedada99.appspot.com
#OAuth Consumer Secret:     YSn7voZOD7XiEGIJdTCs6xbi  
       
              
        
        
              


application = webapp.WSGIApplication([('/', MainPage),('/goauth',GOauth1),('/goauth2',GOauth2)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
