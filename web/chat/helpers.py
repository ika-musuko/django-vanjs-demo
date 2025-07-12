# your_django_file.py
import logging
import requests
from django_eventstream import send_event

logger = logging.getLogger(__name__)

LLM_API_URL = "http://127.0.0.1:8001/generate"

def send_message_and_queue_reply(message):
    _stream_reply_from_llm(message)

def _stream_reply_from_llm(message):
    try:
        with requests.post(
            LLM_API_URL,
            json={"message": message},
            stream=True,
            timeout=30
        ) as response:
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    send_chunk_event(chunk, False)

    except requests.exceptions.RequestException as e:
        logger.error(f"Could not connect to LLM API server: {e}")
        send_chunk_event("Sorry, I encountered an error.", False)

    finally:
        send_chunk_event("", True)

def send_chunk_event(chunk, stop):
    sse_message = {
        "chunk": chunk,
        "stop": stop,
    }
    send_event("botchunk", "message", sse_message)
