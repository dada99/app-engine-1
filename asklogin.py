from google.appengine.api.urlfetch import DownloadError 
from appengine_utilities.sessions import Session
from appengine_utilities.sessions import _AppEngineUtilities_SessionData
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from django.utils import simplejson
import gdata.contacts.client
import oauth
import gdata.docs.service
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
        
class GOauth1(webapp.RequestHandler): 
    def get(self):
        client = gdata.contacts.service.ContactsService()
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
        client = gdata.contacts.client.ContactsClient(source=CONSUMER_KEY)
        session = Session(cookie_name='google-oauth')
        
        if(self.request.get('oauth_token')==''):
            
            
            #client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            #req_token = client.FetchOAuthRequestToken()
            #session['oauth_token_secret'] = req_token.secret
            #client.SetOAuthToken(req_token)
            oauth_callback_url = self.request.uri
            request_token = client.GetOAuthToken(SCOPES, oauth_callback_url, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            session['request_token'] = request_token

            
            # req_token is from previous call to client.GetOAuthToken()
            domain = None  # If on a Google Apps domain, use your domain (e.g. 'example.com').
            self.redirect(request_token.generate_authorization_url(google_apps_domain=domain))
            #self.redirect(client.GenerateOAuthAuthorizationURL(callback_url=oauth_callback_url))



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
        
        #else:
        
        
        
        #access_token=_AppEngineUtilities_SessionData.gql("where id = 354")
        res=db.GqlQuery("select * from _AppEngineUtilities_SessionData where keyname = 'access_token'")
        try:
            access_token=pickle.loads(res.fetch(1)[0].content)
        except IndexError:
            access_token=''
            pass
        #self.response.out.write(access_token)
        if(access_token!=''):
            
            client = gdata.contacts.service.ContactsService() 
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
            #profile feed”µ”–£∫id,title,updated,phonenumber
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
       
              
        
        
              


application = webapp.WSGIApplication([('/', MainPage),('/goauth',GOauth1)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
