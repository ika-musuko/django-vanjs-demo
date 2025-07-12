import asyncio
import random
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()

WORDS = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
    "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
    "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua"
]

class Message(BaseModel):
    message: str

async def random_text_streamer():
    for _ in range(random.randint(50, 200)):
        token = random.choice(WORDS) + " "
        print(token)
        yield token
        await asyncio.sleep(0.05)

@app.post("/generate")
async def stream_random_text(request: Message):
    return StreamingResponse(random_text_streamer(), media_type="text/plain")
