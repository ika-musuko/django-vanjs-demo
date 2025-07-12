import logging
from threading import Thread

from django_eventstream import send_event

from django.core.exceptions import ObjectDoesNotExist

import requests


logger = logging.getLogger(__name__)

LLM_API_URL = "http://127.0.0.1:8001/generate"

from .models import Conversation, Message


def send_conversation_list_update():
    conversations = Conversation.objects \
        .all().order_by("-id") \
        .values("id", "title")
    conversations = list(conversations)
    _send_conversation_list_update_event(conversations)


def send_message_and_queue_reply(conversation_id, message_text):
    title = message_text[:32]
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except ObjectDoesNotExist:
        conversation = Conversation.objects.create(title=title)
        send_conversation_list_update()

    if conversation.title == "New Conversation":
        conversation.title = title
        conversation.save()

    message = Message()
    message.conversation = conversation
    message.from_user = True
    message.text = message_text
    message.save()

    thread = Thread(target=_stream_reply_from_llm, args=(conversation, message_text))
    thread.start()

    print(conversation)
    return conversation.id


def _stream_reply_from_llm(conversation, message):
    try:
        with requests.post(
            LLM_API_URL,
            json={"message": message},
            stream=True,
            timeout=30
        ) as response:
            response.raise_for_status()
            reply = ""
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    reply += chunk
                    _send_chunk_event(chunk, False)

        message = Message()
        message.conversation = conversation
        message.from_user = False
        message.text = reply
        message.save()

    except requests.exceptions.RequestException as e:
        logger.error(f"Could not connect to LLM API server: {e}")
        _send_chunk_event("Sorry, I encountered an error.", False)

    finally:
        _send_chunk_event("", True)


def _send_chunk_event(chunk, stop):
    sse_message = {
        "chunk": chunk,
        "stop": stop,
    }
    send_event("bot_chunk", "message", sse_message)


def _send_conversation_list_update_event(conversations):
    sse_message = {
        "conversations": conversations,
    }
    send_event("conversation_update", "message", sse_message)

