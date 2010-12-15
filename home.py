'''
Created on 2010-12-1

@author: liuda
'''
# coding=utf-8

#from google.appengine.api import users
import time
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
import os
from google.appengine.ext.webapp import template


class Category(db.Model):
    name=db.StringProperty()
    color=db.StringProperty()
    descript=db.TextProperty()     

class Expense(db.Model,webapp.RequestHandler):
    date=db.DateProperty()
    descript=db.TextProperty()
    cate=db.TextProperty()
    num=db.FloatProperty()
    def get(self):
        totalmonth = 0.0
        #if(self.request.get("total")=='true'):
            #if(self.request.get("yearandmon")):
                #for exp in Expense.all():
                    #totalmonth+=exp.num 
        self.response.out.write(self.request.body)
  
    
            
class Home(webapp.RequestHandler):      
    def get(self):
        
        totalmonth = 0.0
        begin=''
        end=''
        if(self.request.get("yearandmon")):
            yearandmon = self.request.get("yearandmon")
            year=yearandmon[:4]
            mon=yearandmon[4:6]
            begin=year+'-'+mon+'-00'
            end=year+'-'+mon+'-31'
            
        query_str = "SELECT * FROM Category"
        if(begin!='' and end!=''):
            query_str2 = "SELECT * FROM Expense where date > :1 and date < :2 order by date DESC" 
            #query_str2 = "SELECT * FROM Expense where num = %f"  % float(90.0)
            #self.response.out.write(query_str2)
        #else:
            #query_str2 = "SELECT * FROM Expense order by date DESC"            
        for exp in Expense.gql("where date = :1",datetime.datetime(2010,12,13)):
            totalmonth+=exp.num
        today = datetime.datetime.today().isoformat()[:10]
        items = db.GqlQuery(query_str)
        items2 = db.GqlQuery(query_str2,(datetime.datetime(2010,12,01),datetime.datetime(2010,12,31)))
        
       
        template_values = {
            'items': items, 
            'items2':items2,
            'today': today, 
            'totalmonth': totalmonth   
        } 
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

            
           
    def post(self):
        itm=Expense()
        d=time.strptime(self.request.get("date").encode('utf-8'),"%Y-%m-%d")
        itm.date=datetime.date(d[0],d[1],d[2])
        itm.descript=self.request.get("descript")
        itm.cate=self.request.get("cate")
        itm.num=float(self.request.get("num").encode('utf-8'))
        itm.put()
        self.redirect('/home') 
        
    def delete(self): 
        deleteitem = self.request.body
        #db.Key(deleteitem)
        #Console.log(deleteitem)
        db.get(deleteitem).delete()
        #self.response.headers['Status'] = '500 Internal Server Error'        
         
           
class Img(db.Model):        
    filename = db.StringProperty(multiline=True)
    file = db.BlobProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    
class Image(webapp.RequestHandler):
    def get(self):
        #query_str = "SELECT * FROM Img"
        #images = db.GqlQuery (query_str)
        img = db.get(self.request.get("img_id"))
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(img.file)
 
class Upload(webapp.RequestHandler):
    def get(self):
        query_str = "SELECT * FROM Img"
        greetings = db.GqlQuery (query_str)

        template_values = {
            'items': greetings,          
        } 
        path = os.path.join(os.path.dirname(__file__), 'upload.htm')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        
        img=Img()

        
        img.file=db.Blob(self.request.body)
        img.put()
        #return 'success'
        #self.redirect('/home/upload')

        
        
        

class Addcate(webapp.RequestHandler):    
    def get(self):
        query_str = "SELECT * FROM Category" 
        items = db.GqlQuery(query_str)
        template_values = {
            'items': items,          
        } 
        path = os.path.join(os.path.dirname(__file__), 'addcate.html')
        self.response.out.write(template.render(path, template_values))
    def post(self): 
        itm=Category()
        itm.name=self.request.get("cate")
        itm.descript=self.request.get("descript")
        
        itm.color=self.request.get("color")
        itm.put()
        self.redirect('/home/addcate')         
         

application = webapp.WSGIApplication([('/home',Home),('/home/',Home),('/home/addcate',Addcate),('/home/upload',Upload),('/home/images',Image),('/home/expense',Expense)], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()