import json

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .helpers import send_message_and_queue_reply


def index(request):
    context = {}
    return render(request, "index.jinja", context)


@require_POST
def send_message(request):
    data = json.loads(request.body)
    message = data["message"]

    send_message_and_queue_reply(message)

    return JsonResponse({}, status=200)
