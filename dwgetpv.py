'''
Created on 2010-12-31

@author: liuda
'''

import os
from google.appengine.api.urlfetch import DownloadError 
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import findpv



class Dwgetpv(webapp.RequestHandler):
    def get(self):
        template_values = {
                       
        } 
        path = os.path.join(os.path.dirname(__file__), 'dwgetpv.html')
        self.response.out.write(template.render(path, template_values))
         
    def post1(self):      
        urlgroup = self.request.get('url')
        urls=urlgroup.split('\r\n')
        out = findpv.findpv(urls)
        output = []
        for i in range(len(out)):
            output.append({"url":urls[i],"pv":out[i]})
        #url="http://www.ibm.com/developerworks/cn/cloud/library/cl-automatevm/"
        #for url in urls:
        template_values = {
           'output':output          
        } 
        path = os.path.join(os.path.dirname(__file__), 'dwgetpv.html')
        self.response.out.write(template.render(path, template_values))
    def post(self):    
        url = self.request.body
        
        out = findpv.findpv(url)
        self.response.out.write(out) 
        #return out
    
application = webapp.WSGIApplication([('/dwpv',Dwgetpv),], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()          


    