"""API Backend avec authentification JWT."""

import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.router import authentification
from src.router import job

load_dotenv()

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
ALLOWED_ORIGINS = json.loads(os.getenv("ALLOWED_ORIGINS", '["http://localhost:5173"]'))


app = FastAPI(title="Backend API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentification.router)
app.include_router(job.router)


@app.get("/")
async def root():
    return {"message": "API opérationnelle", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    print(f"🚀 API sur http://{API_HOST}:{API_PORT}")
    print(f"📚 Docs sur http://{API_HOST}:{API_PORT}/docs")
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=True)
