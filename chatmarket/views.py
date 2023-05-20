from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from gaia import settings


# Create your views here.
@csrf_exempt
def meta_wa_callbackurl(request):
    if request.method == "POST":
        try:
            print('POST: Someone is pinging me!')
            return HttpResponse(status=200)
        except Exception as error:
            print({'error': error})
            return HttpResponseServerError()
    try:
        print('GET: Someone is pinging me!')
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode and token and mode == 'subscribe' and settings.META_WA_VERIFY_TOKEN == token:
            return HttpResponse(challenge)
        else:
            return HttpResponseForbidden()
    except Exception as error:
        print({'error': error})
        return HttpResponseServerError()
