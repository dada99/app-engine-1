'''
Created on 2010-12-28

@author: liuda
'''

from pymongo import Connection
import time




def mongotest():
    connection = Connection()
    db = connection.test
    #print db.test.find_one()
    with open('mongotestdb.txt', 'r') as f:
        read_data = f.readlines()
    f.closed
    item=["parentID","myID","userName","userID","content","date"]
    
    all=[] 
    for line in read_data:
        cache = {} 
        l = line.split('\t')
        for i in range(len(l)):
            cache[item[i]]=l[i]
        #print cache            
        all.append(cache)    
    db.mongo.insert(all)  
    #print all        
           
   
      

 


    
    


if __name__ == '__main__':
    mongotest()