from django.http import HttpResponse
import json

from TTsys import *

def getSystemInfo(request):
    rs = {"CPU":getCPUstate(),"RAM":getMemorystate(),"NET":getNetsate()}
    return HttpResponse(json.dumps(rs))