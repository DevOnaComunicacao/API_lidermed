import jwt
import os
import datetime
import dotenv
import requests
from fastapi import Header, HTTPException
from fastapi.responses import JSONResponse

dotenv.load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

admin = os.getenv('ADMIN')
password = os.getenv('PASS')

def criar_tokens(user):
    secret = os.getenv('JWT_KEY')

    token = jwt.encode({
        'user_id': user,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow(),
    }, secret, algorithm='HS256')
    return token

def validar_login(user):
    try:
        if user.usuario == admin and user.senha == password:
            token = criar_tokens(user.usuario)
            return JSONResponse(content={'token': token})
        else:
            return JSONResponse(content={'erro': 'credenciais inválidas'})
    except Exception as e:
        return JSONResponse(content={'erro': str(e)})

def validar_tokens(authorization: str = Header(None)):

    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Token não enviado")

        token = authorization.split(" ")[1]

        payload = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def criar_token_kommo():
    url = os.getenv('KOMMO_URL_AUTH')
    data = {
        "client_id": os.getenv("KOMMO_CLIENT_ID"),
        "client_secret": os.getenv("KOMMO_CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("REFRESH_TOKEN"),
        "redirect_uri": os.getenv("KOMMO_URL")
    }
    res = requests.post(url, data=data)
    res.raise_for_status()
    return res.json()["access_token"]