
from appengine_utilities.sessions import Session
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import urllib
import oauth
import gdata.docs.service

import gdata.auth

CONSUMER_KEY = 'thedada99.appspot.com'
CONSUMER_SECRET = 'YSn7voZOD7XiEGIJdTCs6xbi'
SCOPES = ['https://docs.google.com/feeds/', 'https://www.google.com/calendar/feeds/']
SIG_METHOD = 'gdata.auth.OAuthSignatureMethod.HMAC_SHA1'
        #self.redirect('/')
        
class GOauth1(webapp.RequestHandler): 
    def get(self):
        
        
        if(self.request.get('oauth_token')==''):
            session = Session()
            client = gdata.docs.service.DocsService(source=CONSUMER_KEY)
            client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
            req_token = client.FetchOAuthRequestToken()
            session['oauth_token_secret'] = req_token.secret
            client.SetOAuthToken(req_token)
            oauth_callback_url = self.request.uri
            
            
            self.redirect(client.GenerateOAuthAuthorizationURL(callback_url=oauth_callback_url))



        else:
            session = Session()
            oauth_token = gdata.auth.OAuthTokenFromUrl(self.request.uri)
            client = gdata.docs.service.DocsService(source=CONSUMER_KEY)
            if oauth_token:
                
                oauth_token.secret = session['oauth_token_secret']
                #print oauth_token.secret
                #oauth_token.oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                client.SetOAuthToken(oauth_token)
                #print client._oauth_input_params
                access_token = client.UpgradeToOAuthAccessToken()
                if access_token and users.get_current_user():
                    client.token_store.add_token(access_token)
                elif access_token:
                    client.current_token = access_token
                    client.SetOAuthToken(access_token)
                #client.SetOAuthToken(access_token)
                client = gdata.docs.service.DocsService() 
                client.SetOAuthInputParameters(SIG_METHOD, CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
                #client1.SetOAuthToken(gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret))
                oauth_input_params = gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1,CONSUMER_KEY, consumer_secret=CONSUMER_SECRET) 
                oauth_token = gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret, oauth_input_params=oauth_input_params) 
                client.SetOAuthToken(oauth_token) 
                feed = client.GetDocumentListFeed()
                for entry in feed.entry:
                    print entry.title.text



                
                
                
                
       
                #for entry in feed.entry:
                    #print entry.title.text


                
                
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
        self.response.out.write('Go to <a href="/goauth">Google OAuth Sample</a>')
        
        #else:
            
            
#OAuth Consumer Key:     thedada99.appspot.com
#OAuth Consumer Secret:     YSn7voZOD7XiEGIJdTCs6xbi  
       
              
        
        
              


application = webapp.WSGIApplication([('/', MainPage),('/goauth',GOauth1)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
