import datetime
import time
import os.path

from django.utils import timezone
from django.http import HttpResponse


def current_datetime():
    now = datetime.datetime.now()
    html = "<html><body>On server, now it is %s (%f), tz = %s.</body></html>" % (now, time.time(), timezone.now())
    return HttpResponse(html)


def index(request):
    return current_datetime()


def get_headers(request):
    """To investigate how to redirect request from http"""
    # HTTP_X_FORWARDED_PROTO: if http it should be redirected to https
    headers = ['%s: %s' % (k, v) for k, v in request.META.items()]
    return HttpResponse('\n'.join(headers))


def source_version(request):
    """Read from source_tip.txt"""
    TIP_FILE = 'app1/source_tip.txt'
    content = 'not specified'
    if os.path.exists(TIP_FILE):
        with open(TIP_FILE, 'r') as tip:
            content = tip.read()
    return HttpResponse(content)
