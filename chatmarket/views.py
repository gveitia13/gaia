import json
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
        data = json.loads(request.body)
        print("Received webhook data: %s", data)
        changed_field = messenger.changed_field(data)
        if changed_field == "messages":
            new_message = messenger.get_mobile(data)
            if new_message:
                mobile = messenger.get_mobile(data)
                name = messenger.get_name(data)
                message_type = messenger.get_message_type(data)
                print(
                    f"New Message; sender:{mobile} name:{name} type:{message_type}"
                )
                if message_type == "text":
                    message = messenger.get_message(data)
                    name = messenger.get_name(data)
                    print("Message: %s", message)
                    messenger.send_message(f"Hi {name}, nice to connect with you", mobile)
                elif message_type == "interactive":
                    message_response = messenger.get_interactive_response(data)
                    interactive_type = message_response.get("type")
                    message_id = message_response[interactive_type]["id"]
                    message_text = message_response[interactive_type]["title"]
                    print(f"Interactive Message; {message_id}: {message_text}")
                elif message_type == "location":
                    message_location = messenger.get_location(data)
                    message_latitude = message_location["latitude"]
                    message_longitude = message_location["longitude"]
                    print("Location: %s, %s", message_latitude, message_longitude)
                elif message_type == "image":
                    image = messenger.get_image(data)
                    image_id, mime_type = image["id"], image["mime_type"]
                    image_url = messenger.query_media_url(image_id)
                    image_filename = messenger.download_media(image_url, mime_type)
                    print(f"{mobile} sent image {image_filename}")
                elif message_type == "video":
                    video = messenger.get_video(data)
                    video_id, mime_type = video["id"], video["mime_type"]
                    video_url = messenger.query_media_url(video_id)
                    video_filename = messenger.download_media(video_url, mime_type)
                    print(f"{mobile} sent video {video_filename}")
                elif message_type == "audio":
                    audio = messenger.get_audio(data)
                    audio_id, mime_type = audio["id"], audio["mime_type"]
                    audio_url = messenger.query_media_url(audio_id)
                    audio_filename = messenger.download_media(audio_url, mime_type)
                    print(f"{mobile} sent audio {audio_filename}")
                elif message_type == "document":
                    file = messenger.get_document(data)
                    file_id, mime_type = file["id"], file["mime_type"]
                    file_url = messenger.query_media_url(file_id)
                    file_filename = messenger.download_media(file_url, mime_type)
                    print(f"{mobile} sent file {file_filename}")
                else:
                    print(f"{mobile} sent {message_type} ")
                    print(data)
            else:
                delivery = messenger.get_delivery(data)
                if delivery:
                    print(f"Message : {delivery}")
                else:
                    print("No new message")
        data = messenger.get_message(request.POST)
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
