import datetime
import logging
import time
import os.path

from django.utils import timezone
from django.http import HttpResponse


logger = logging.getLogger(__name__)

def current_datetime():
    now = datetime.datetime.now()
    html = "<html><body>On server, now it is %s (%f), tz = %s.</body></html>" % (now, time.time(), timezone.now())
    return HttpResponse(html)


def index(request):
    logger.debug('index call, return times')
    return current_datetime()


def get_headers(request):
    """To investigate how to redirect request from http"""
    # HTTP_X_FORWARDED_PROTO: if http it should be redirected to https
    headers = ['%s: %s' % (k, v) for k, v in request.META.items()]
    return HttpResponse('\n'.join(headers))


def source_version(request):
    """Read from source_tip.txt"""
    tip_file = __name__.split('.')[0] + '/source_tip.txt'
    content = 'not specified'
    if os.path.exists(tip_file):
        with open(tip_file, 'r') as tip:
            content = tip.read()
    return HttpResponse(content)
