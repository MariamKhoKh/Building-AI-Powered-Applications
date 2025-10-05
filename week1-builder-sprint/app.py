from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

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

class ChatResponse(BaseModel):
    response: str

class HealthResponse(BaseModel):
    status: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message is required")

        response = model.generate_content(request.message)

        return ChatResponse(response=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok")
