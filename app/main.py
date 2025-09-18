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

