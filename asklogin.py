
from appengine_utilities.sessions import Session
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import urllib
import oauth
import gdata.docs
import gdata.auth
import gdata.docs.service
gd_client = gdata.docs.service.DocsService()
CONSUMER_KEY = 'thedada99.appspot.com'
CONSUMER_SECRET = 'YSn7voZOD7XiEGIJdTCs6xbi'
class GOauth(webapp.RequestHandler):
    def get(self):
        #self.session = Session()
        
        
        if(self.request.get('oauth_token')==''):
            self.session = Session()
            gd_client.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1,CONSUMER_KEY, CONSUMER_SECRET)
            request_token = gd_client.FetchOAuthRequestToken(oauth_callback=self.request.uri)
            self.session['oauth_token_secret'] = request_token
            gd_client.SetOAuthToken(request_token)
            domain = self.request.get('domain', default_value='default')
            auth_url = gd_client.GenerateOAuthAuthorizationURL(extra_params={'hd': domain})
            self.redirect(auth_url)
        else:
            self.session = Session()
            oauth_token = gdata.auth.OAuthTokenFromUrl(self.request.uri)
            if oauth_token:
                oauth_token.secret = self.session['oauth_token_secret']
                oauth_token.oauth_input_params = gd_client.GetOAuthInputParameters()
                gd_client.SetOAuthToken(oauth_token)

                # 3.) Exchange the authorized request token for an access token
                oauth_verifier = self.request.get('oauth_verifier', default_value='')
                access_token = gd_client.UpgradeToOAuthAccessToken()

                # Remember the access token in the current user's token store
                if access_token and users.get_current_user():
                    gd_client.token_store.add_token(access_token)
                elif access_token:
                    gd_client.current_token = access_token
                    gd_client.SetOAuthToken(access_token) 
        #self.redirect('/')
        
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
       
              
        
        
              


application = webapp.WSGIApplication([('/', MainPage),('/goauth',GOauth)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
