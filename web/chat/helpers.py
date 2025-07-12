import logging
logger = logging.getLogger(__name__)

from django_eventstream import send_event


def send_message_and_queue_reply(message):
    _reply_to(message)

def _reply_to(message):
    reply = message
    send_reply_event(reply)

def send_reply_event(reply):
    sse_message = {
        "reply": reply
    }
    send_event("reply", "message", sse_message)

