# coding=utf-8

import urllib2
import time

def findpv(urls):
    output=[]
    for url in urls:
        a=[]
        try:
            a=urllib2.urlopen(url).readlines(16000)
        except IOError:
            print 'cannot open', url
        
        b=('').join(a)
        word=u'访问情况</b>&nbsp;'.encode('utf-8')
        position=b.find(word)
        if position > 0:
            tmp = b[position+22:position+30]
            last=0
            for i in range(len(tmp)):
                if tmp[i] not in ('1','2','3','4','5','6','7','8','9','0'):
                    last = i
                    break
            output.append(tmp[0:last])
    return output  


if __name__ == "__main__": 
    url="http://www.ibm.com/developerworks/cn/cloud/library/cl-automatevm/"
    starttime=time.time()
    findpv(url)
    endtime=time.time()
    print endtime - starttime