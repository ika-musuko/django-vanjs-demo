import logging
logger = logging.getLogger(__name__)

from time import sleep

from django_eventstream import send_event

from .utils import chunker


def send_message_and_queue_reply(message):
    _reply_to(message)

def _reply_to(message):
    reply = (message + " ") * 100
    _chunk_message(reply)


def _chunk_message(message):
    for char in chunker(message, 5):
        sleep(0.005)
        send_chunk_event(char, False)
    send_chunk_event("", True)

def send_chunk_event(chunk, stop):
    sse_message = {
        "chunk": chunk,
        "stop": stop,
    }
    send_event("botchunk", "message", sse_message)

