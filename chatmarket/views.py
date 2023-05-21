from collections import defaultdict

from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chatmarket.models import EcommerceStore
from gaia import settings
from heyoo import WhatsApp
import os
messenger = WhatsApp( settings.META_WA_ACCESSTOKEN,  phone_number_id=settings.META_WA_SENDER_PHONE_NUMER_ID)
print('messenger')
Store = EcommerceStore()
print('Store')
CustomerSession = defaultdict(dict)
print('CustomerSession')
# Create your views here.
@csrf_exempt
def meta_wa_callbackurl(request):
    if request.method == "POST":
        # try:
        print(request.POST)
        data = messenger.get_message(request.POST)
        print('data')
        print(data)
        # if data and data.get("isMessage"):
        #     incomingMessage = data["message"]
        #     recipientPhone = incomingMessage["from"]["phone"]
        #     recipientName = incomingMessage["from"]["name"]
        #     typeOfMsg = incomingMessage["type"]
        #     message_id = incomingMessage["message_id"]
        print('POST: Someone is pinging me!')
        return HttpResponse(status=200)
        # except Exception as error:
        #     print({'error': error})
        #     return HttpResponseServerError()
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
