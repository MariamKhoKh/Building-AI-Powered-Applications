from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

class ChatRequest(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str

async def generate_stream(message: str):
    try:
        response = model.generate_content(message, stream=True)
        
        # Stream the text chunks
        for chunk in response:
            if chunk.text:
                yield f"data: {json.dumps({'type': 'chunk', 'text': chunk.text})}\n\n"
        
        # Send usage metadata at the end
        # Resolve the response to get usage metadata
        response.resolve()
        
        if hasattr(response, 'usage_metadata'):
            usage_data = {
                'type': 'metadata',
                'inputTokens': response.usage_metadata.prompt_token_count,
                'outputTokens': response.usage_metadata.candidates_token_count,
                'totalTokens': response.usage_metadata.total_token_count
            }
            yield f"data: {json.dumps(usage_data)}\n\n"
        
        yield "data: {\"type\": \"done\"}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    return StreamingResponse(
        generate_stream(request.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")