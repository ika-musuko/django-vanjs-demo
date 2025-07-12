import logging
import markovify
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

text_model = None
try:
    corpus_file = "1342-0.txt"
    logger.info(f"⏰️ Building Markovify model from {corpus_file}...")
    with open(corpus_file, encoding="utf-8") as f:
        text_model = markovify.Text(f.read(), state_size=2)
    logger.info(f"✅ Markovify model built successfully from {corpus_file}")
except FileNotFoundError:
    logger.error(f"❌ {corpus_file} not found. Markovify model could not be built.")
except Exception as e:
    logger.error(f"❌ An error occurred while building the model: {e}")

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/generate")
def generate_sentence(request: Message):
    """
    Generates a sentence with a max length based on the input message's length.
    """
    if not text_model:
        raise HTTPException(status_code=503, detail="Markov model is not available.")

    reply = text_model.make_sentence_with_start(request.message.split(" ")[0])

    if not reply:
        reply = "I'm not quite sure what to say about that."

    return {"reply": reply}
