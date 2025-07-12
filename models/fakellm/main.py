import logging
import queue
import threading
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None
tokenizer = None
try:
    model_name = "distilgpt2"
    logger.info(f"⏰️ Loading pre-trained model '{model_name}'...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    logger.info(f"✅ Model '{model_name}' loaded successfully.")
except Exception as e:
    logger.error(f"❌ Failed to load model: {e}")

class ThreadedTextStreamer(TextStreamer):
    def __init__(self, tokenizer, q):
        super().__init__(tokenizer)
        self.q = q
        self.previous_text = ""

    def on_finalized_text(self, text: str, stream_end: bool = False):
        new_text = text[len(self.previous_text):]
        self.previous_text = text
        if new_text:
            self.q.put(new_text)
        if stream_end:
            self.q.put(None)

app = FastAPI()

class Message(BaseModel):
    message: str

def generation_thread(prompt, streamer):
    """Runs the model generation in a separate thread with better parameters."""
    inputs = tokenizer(prompt, return_tensors="pt")
    model.generate(
        **inputs,
        streamer=streamer,
        do_sample=True,
        max_new_tokens=250,
        temperature=0.8,
        top_k=50,
        repetition_penalty=1.2,
        eos_token_id=tokenizer.eos_token_id
    )

def stream_generator(prompt: str):
    """Yields tokens from the queue as they are generated."""
    q = queue.Queue()
    streamer = ThreadedTextStreamer(tokenizer, q)
    thread = threading.Thread(target=generation_thread, args=(prompt, streamer))
    thread.start()
    while True:
        token = q.get()
        if token is None or token == tokenizer.eos_token:
            break
        yield token

@app.post("/generate")
def generate_reply(request: Message):
    if not model or not tokenizer:
        raise HTTPException(status_code=503, detail="Text generation model is not available.")

    return StreamingResponse(stream_generator(request.message), media_type="text/plain")
