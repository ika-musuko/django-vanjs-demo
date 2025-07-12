import json

from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .helpers import send_conversation_list_update, send_message_and_queue_reply

from .models import Conversation


def index(request):
    conversations = Conversation.objects.all().order_by("-id")

    context = {
        "conversations": conversations
    }

    return render(request, "index.jinja", context)


@require_GET
def get_conversation_messages(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)

    context = {
        "messages": list(conversation.messages.all().values("from_user", "text"))
    }

    return JsonResponse(context, status=200)


@require_POST
def new_conversation(request):
    Conversation.objects.create(title="New Conversation")
    send_conversation_list_update()
    return JsonResponse({}, status=200)


@require_POST
def send_message(request):
    data = json.loads(request.body)
    conversation_id = data["conversation_id"]
    message = data["message"]

    conversation_id = send_message_and_queue_reply(conversation_id, message)

    return JsonResponse({"conversation_id": conversation_id}, status=200)
