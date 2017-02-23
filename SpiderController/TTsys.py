import psutil 

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