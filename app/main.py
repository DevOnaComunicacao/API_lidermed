from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.models import Interessados, Compradores, Admin
from app.auth import validar_login, validar_tokens
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

@app.post("/login")
def post_login(admin: Admin):
    return validar_login(admin)

@app.post("/lidermedtech")
def post_lidermedtech(interessados: Interessados, auth: dict = Depends(validar_tokens)):
    return handler_lidermedtech(interessados)

@app.post("/lidermed")
def post_lidermed(compradores: Compradores):

    return handler_lidermed(compradores)

