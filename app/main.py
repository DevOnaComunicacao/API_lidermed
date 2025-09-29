import threading
import requests
import os
import jwt
import dotenv
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from app.models import Interessados, Compradores, Admin
from app.auth import validar_login, gerar_callback
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

origins = [
    "https://www.lidermed.com.br",
    "https://lidermed.com.br"
    "https://lidermedtech.com.br",
    "https://www.lidermedtech.com.br"
]

@app.get('/')
def root():
    return {'status': 'servidor rodando'}

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/kommo/callback')
def get_kommo_callback(request: Request):
    return gerar_callback(request)

@app.post('/login')
def post_login(admin: Admin):
    return validar_login(admin)

@app.post('/lidermedtech')
def post_lidermedtech(interessados: Interessados, request: Request):
    origin = request.headers.get("origin")

    if origin in origins:
        return handler_lidermedtech(interessados)

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {"erro": "Token não enviado"}

    try:
        secret = os.getenv('JWT_KEY')
        payload = jwt.decode(
            auth_header.split(" ")[1],
            secret,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return {"erro": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"erro": "Token inválido"}

    return handler_lidermedtech(interessados)


@app.post('/lidermed')
def post_lidermed(compradores: Compradores, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return {"erro": "Token não enviado"}

    try:

        secret = os.getenv('JWT_KEY')

        payload = jwt.decode(
            auth_header.split(" ")[1],
            secret,
            algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        return {"erro": "Token expirado"}
    except jwt.InvalidTokenError:
        return {"erro": "Token inválido"}

    return handler_lidermed(compradores)

