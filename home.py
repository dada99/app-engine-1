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
            #yearandmon 是YYYY-M or YYYY-MM 的形式
            yearandmon = self.request.get("yearandmon")
            yearandmon=yearandmon.encode('utf-8').split('-')
            
            year=int(yearandmon[0])
            mon=int(yearandmon[1])
            
            begin=datetime.date(year,mon,01)
            
            if(mon==12):
                end=datetime.date(year+1,1,01)
            else:
                end=datetime.date(year,mon+1,01)    
            #如果月份为12月，那么end就要变成下一年的1月1日。
        query_str = "SELECT * FROM Category"
        if(begin!='' and end!=''):
            #items2 = db.GqlQuery("SELECT * FROM Expense where date > '%s' and date < '%s' order by date DESC" % (datetime.date(2010,9,1),datetime.date(2010,10,1)))
            items2 =  Expense.gql("where date > :1 and date < :2",begin,end)
            #注意gql搜索的写法，qgl(query,arg1,arg2,....),基本放弃GqlQuery，：《
            
        else:
            items2 = db.GqlQuery("SELECT * FROM Expense order by date DESC")            
        for exp in items2:
            totalmonth+=exp.num
        #总计的金额根据返回条目来计算，如果是月视图，就计算当月的花费            
        todayfull = datetime.datetime.today().isoformat()
        today=todayfull[:10]
        
        items = db.GqlQuery(query_str)
        
        
        
       
        template_values = {
            'items': items, 
            'items2':items2,
            'today': today, 
            'totalmonth': totalmonth,
            
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