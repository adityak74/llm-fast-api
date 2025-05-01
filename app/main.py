from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.chat_controller import router as chat_router

app = FastAPI(
    title="LLM FastAPI Server",
    description="OpenAI-compatible API server using local LLM",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "LLM FastAPI Server is running"} 