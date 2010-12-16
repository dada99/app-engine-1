'''
Created on 2010-12-16

@author: liuda
'''
import urllib
import oauth
import gdata.contacts
import gdata.contacts.service

CONSUMER_KEY = 'yourdomain.com'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
CONTACTS_URL = 'http://www.google.com/m8/feeds/contacts/default/full'

# Setup 2 legged OAuth consumer based on our admin "credentials"
consumer = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)

user = 'thedada99'
params = {'max-results': 50, 'xoauth_requestor_id': user}

# Construct the request manually and sign it using HMAC-SHA1
# Note: The params dictionary needs to be passed in separately from the base URL
request = oauth.OAuthRequest.from_consumer_and_token(
   consumer, http_method='GET', http_url=CONTACTS_URL, parameters=params)
request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, None)

# See patch @ http://code.google.com/p/oauth/issues/detail?id=31
headers = request.to_header()

#client = gdata.contacts.service.ContactsService()

# Query the user's contacts and print their name & email
#uri = '%s?%s' % (request.http_url, urllib.urlencode(params))
#feed = client.GetFeed(uri, extra_headers=headers, converter=gdata.contacts.ContactsFeedFromString)
#for entry in feed.entry:
    #print '%s, %s' % (entry.title.text, entry.email[0].address)
    
    
