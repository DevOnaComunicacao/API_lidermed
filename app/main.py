import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Interessados, Compradores
from app.handlers import handler_lidermedtech, handler_lidermed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # pega a porta do Render
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)

@app.get("/")
def root():
    return {"status": "servidor rodando"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/lidermedtech")
def post_lidermedtech(interessados: Interessados):
    return handler_lidermedtech(interessados)

@app.post("/lidermed")
def post_lidermed(compradores: Compradores):

    return handler_lidermed(compradores)
