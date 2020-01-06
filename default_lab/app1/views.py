import datetime
import logging
import os
import os.path
import time

from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.conf import settings


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


def display_envs(request):
    envs = ['%s: %s' % (k, v) for k, v in os.environ.items()]
    return HttpResponse('\n'.join(envs))


def source_version(request):
    """Read from source_tip.txt"""
    tip_file = __name__.split('.')[0] + '/source_tip.txt'
    content = 'not specified'
    if os.path.exists(tip_file):
        with open(tip_file, 'r') as tip:
            content = tip.read()
    return HttpResponse(content)


def oauth(request):
    host =  os.getenv('GAE_SERVICE', '') + '-' + os.getenv('GAE_VERSION', '')
    if host.strip() == '-':
        host = 'localhost is your target?'
    return HttpResponse(F"You have been redirected to here to see your host: {host}")


def oauth_redirect(request):
    logger.debug(settings.OAUTH2_REDIRECT_URL)
    return HttpResponse(F"This is your redirect url set in settings {settings.OAUTH2_REDIRECT_URL}")


def client(request):
    """Get client information """
    # REMOTE_ADDR will be useless once behind a proxy like in GAE

    # https://cloud.google.com/appengine/docs/flexible/python/reference/request-headers
    GAE_HEADERS = {
        "HTTP_USER_AGENT": "User_Agent",
        "HTTP_X_FORWARDED_FOR": "Remote_addr",
        "HTTP_X_APPENGINE_CITY": "City",
        "HTTP_X_APPENGINE_REGION": "Region",
        "HTTP_X_APPENGINE_COUNTRY": "Country",
        "HTTP_X_APPENGINE_CITYLATLONG": "Latlong"
    }

    try:
        if "HTTP_X_APPENGINE_CITYLATLONG" in request.META:
            # On GAE
            info = {GAE_HEADERS[k]: request.META[k] for k in GAE_HEADERS.keys()}
            # Use client IP, the first IP as Remote_addr
            info["Remote_addr"] = info["Remote_addr"].split(",")[0].strip()
            # Split Latlong into Latitude and Longitude and keep Latlong for Google Maps API
            info["Latitude"], info["Longitude"] = info["Latlong"].split(",")
        else:
            info = {
                "User_Agent": request.META["HTTP_USER_AGENT"],
                "Remote_addr": request.META["REMOTE_ADDR"]
            }
    except KeyError:
        info = {}
        for k, v in request.META.items():
            if isinstance(v, str):
                info[k] = v

    return JsonResponse(info)
