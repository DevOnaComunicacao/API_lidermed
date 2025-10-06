import jwt
import os
import datetime
import dotenv
import requests
from fastapi import Header, HTTPException, Request
from fastapi.responses import JSONResponse
from app.bd import get_mysql_connection
from pathlib import Path

if os.getenv("RENDER") != "true":
    env_path = Path(__file__).parent / ".env"
    dotenv.load_dotenv(dotenv_path=env_path)
    print("Carregando .env localmente")
else:
    print("Rodando no Render, .env ignorado")

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
            raise HTTPException(status_code=401, detail='Token não enviado')

        token = authorization.split(' ')[1]

        payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256'])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expirado')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Token inválido')


def criar_token_kommo():

    conn = get_mysql_connection()
    if conn is None:
        raise RuntimeError("Falha ao conectar no banco.")

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT token FROM tokens LIMIT 1;")
        resultado = cursor.fetchone()

        if not resultado:
            raise ValueError("Nenhum refresh token encontrado na tabela 'tokens'.")

        refresh_token = resultado[0].strip()
        print(f"Usando refresh token: {refresh_token}")

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    # --- Request para Kommo ---
    url = os.getenv('KOMMO_URL_AUTH', '').strip()
    data = {
        'client_id': os.getenv('KOMMO_CLIENT_ID', '').strip(),
        'client_secret': os.getenv('KOMMO_CLIENT_SECRET', '').strip(),
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': os.getenv('KOMMO_REDIRECT_URI', '').strip()
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        res = requests.post(url, data=data, headers=headers)
        res.raise_for_status()
        resp_json = res.json()

        access_token = resp_json.get('access_token')
        novo_refresh_token = resp_json.get('refresh_token')  # chave nova, importante!

        if not access_token:
            raise ValueError("Nenhum access token retornado pelo Kommo.")

        # --- Atualiza refresh token no banco se houver novo ---
        if novo_refresh_token and novo_refresh_token != refresh_token:
            conn = get_mysql_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE tokens SET token = %s;", (novo_refresh_token,))
            conn.commit()
            cursor.close()
            conn.close()
            print("Refresh token atualizado no banco.")

        return access_token

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Falha na requisição de token Kommo: {e}")

def gerar_callback(request):
    code = request.query_params.get("code")
    if not code:
        return {"erro": "Nenhum código recebido"}

    token_url = f"{os.getenv('KOMMO_URL')}/oauth2/access_token"

    payload = {
        "client_id": os.getenv("KOMMO_CLIENT_ID"),
        "client_secret": os.getenv("KOMMO_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("KOMMO_REDIRECT_URI"),
    }

    # ⚠️ O Kommo exige form-data, não JSON
    res = requests.post(token_url, data=payload)
    data = res.json()

    if "access_token" in data and "refresh_token" in data:
        dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")

        # Atualiza ou cria as variáveis no .env
        dotenv.set_key(dotenv_path, "KOMMO_ACCESS_TOKEN", data["access_token"])
        dotenv.set_key(dotenv_path, "KOMMO_REFRESH_TOKEN", data["refresh_token"])

        return {"status": "ok", "tokens": data}
    else:
        return {"erro": "Não foi possível gerar o token", "detalhe": data}
