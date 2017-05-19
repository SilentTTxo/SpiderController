import psutil 
import urllib2

import json

def getCPUstate(interval=1):  
    return (str(psutil.cpu_percent(interval)) + "%")
def getMemorystate():   
        phymem = psutil.virtual_memory()  
        line = "%6s/%s"%(  
            str(int(phymem.used/1024/1024)),  
            str(int(phymem.total/1024/1024))  
            )  
        return line
def getNetsate():
    net = psutil.net_io_counters()  
    bytes_sent = '{0:.2f}'.format(net.bytes_recv / 1024 /1024)  
    bytes_rcvd = '{0:.2f}'.format(net.bytes_sent / 1024 /1024)  
    return "%s %s"%(bytes_rcvd, bytes_sent)

def checkIp(proxy):
    url = 'http://httpbin.org/get?show_env=1'
    proxy_support = urllib2.ProxyHandler({'http':proxy})
    opener = urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
    req = urllib2.Request(url,headers=i_headers)
    try:
        html = urllib2.urlopen(req,timeout=2)
        if url == html.geturl():
            doc = html.read()
            doc = json.loads(doc)
            if(doc['origin'] == proxy.split(":")[0]):
                return True
            else:
                return False
    except Exception, e:
        return False