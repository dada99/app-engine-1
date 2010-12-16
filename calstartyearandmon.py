'''
Created on 2010-12-15

@author: liuda
'''


def calstartyearandmon(year,mon,x):
    
    if(mon<x):
        start_mon=mon-x+12
        start_year=year-1
        mon=start_mon
        year=start_year
        if(mon<0):
            calstartyearandmon(year,abs(mon),x-12)
    else:
        start_mon=mon-x
        start_year=year
        
    return start_year,start_mon      