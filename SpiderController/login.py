from django.http import HttpResponseRedirect
from conf import conf
import urllib
import json
import os
from django.views.decorators.csrf import csrf_exempt
from SpiderModel.models import User

def isLogin(fn):
    @csrf_exempt
    def wrapped(request):
        if(request.session.get('uid',None) == None):
            return HttpResponseRedirect(conf.login_url)
        else:
            return fn(request)
    return wrapped

def isAdmin(fn):
    def wrapped(request):
        try:
            if(request.session['power'] != -1):
                return HttpResponse("you are not admin")
            return fn(request)
        except:
            return HttpResponseRedirect(conf.login_url)
    return wrapped