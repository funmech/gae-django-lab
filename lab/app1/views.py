import datetime
import time

from django.utils import timezone
from django.http import HttpResponse


def current_datetime():
    now = datetime.datetime.now()
    html = "<html><body>On server, now it is %s (%f), tz = %s.</body></html>" % (now, time.time(), timezone.now())
    return HttpResponse(html)


def index(request):
    return current_datetime()


def headers(request):
    """To investigate how to redirect request from http"""
    # HTTP_X_FORWARDED_PROTO: if http it should be redirected to https
    headers = ['%s: %s' % (k, v) for k, v in request.META.items()]
    return HttpResponse('\n'.join(headers))
