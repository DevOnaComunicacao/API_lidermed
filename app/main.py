import threading
import requests
import os
import jwt
import dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models import Interessados, Compradores
from app.auth import gerar_callback
from app.handlers import handler_lidermedtech, handler_lidermed

app = FastAPI()

if os.getenv("RENDER") != "true":
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    dotenv.load_dotenv(dotenv_path)
    print("Carregando .env localmente")
else:
    print("Rodando no Render, .env ignorado")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def ping_servidor():
    try:
        requests.get("https://api.lidermedtech.com.br")
    except Exception as e:
        print("Erro no ping:", e)
    threading.Timer(13 * 60, ping_servidor).start()

@app.on_event("startup")
def iniciar_ping():
    ping_servidor()

@app.get('/')
def root():
    return {'status': 'servidor rodando'}

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/kommo/callback')
def get_kommo_callback(request: Request):
    return gerar_callback(request)

@app.post('/lidermedtech')
def post_lidermedtech(interessados: Interessados):
    return handler_lidermedtech(interessados)

@app.post('/lidermed')
async def post_lidermed(compradores: Compradores, request: Request):
    data = await request.json()
    print("Payload recebido:", data)
    return handler_lidermed(compradores)




