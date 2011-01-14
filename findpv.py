# coding=utf-8
"""
本程序用于抓取developerworks中国网站文章和教程的访问数据。访问数据是自动由程序从后台生成的，本程序就是要对页面进行解析，并找到
相应的字段，读取访问数据，然后进行返回。
"""
import urllib2
import time
from google.appengine.api.urlfetch import DownloadError 

"""
findpv_old 为批量读取的版本，输入为一个url列表，输出为对应的访问数量。
"""
def findpv_old(urls):
    output=[]
    for url in urls:
        a=[]
        try:
            a=urllib2.urlopen(url).readlines(16000)#读取URL指向页面的前16000个字节，经过测算，只有到了这个大小才能读取到访问数据
        except DownloadError:
            return 'cannot open this'
        
        b=('').join(a)
        word=u'访问情况</b>&nbsp;'.encode('utf-8')#使用utf-8的格式才能顺利进行find搜索
        position=b.find(word)
        if position > 0:
            tmp = b[position+22:position+30]#position+22:position+30也是经验数据，在定位了'访问情况'字段以后，需要往后读取22个字节才是访问的数据值。
            last=0
            for i in range(len(tmp)):#为了避免读取多余的内容，将非数字进行过滤
                if tmp[i] not in ('1','2','3','4','5','6','7','8','9','0'):
                    last = i
                    break
            output.append(tmp[0:last])
    return output  


def findpv(url):
    a=[]
    try:
        a=urllib2.urlopen(url).readlines(16000)
    except DownloadError:
        return '<b>cannot open this</b>'
    
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
        #output.append(tmp[0:last])
        return tmp[0:last]
    else:
        return '<b>invalid input</b>'


if __name__ == "__main__": 
    url="http://www.ibm.com/developerworks/cn/cloud/library/cl-automatevm/"
    starttime=time.time()
    findpv(url)
    endtime=time.time()
    print endtime - starttime