import jwt
import os
import datetime
import dotenv
import requests
from fastapi import Header, HTTPException, Request
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
            raise HTTPException(status_code=401, detail='Token não enviado')

        token = authorization.split(' ')[1]

        payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256'])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expirado')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Token inválido')


#def criar_token_kommo():
    url = os.getenv('KOMMO_URL_AUTH')
    data = {
        'client_id': os.getenv('KOMMO_CLIENT_ID'),
        'client_secret': os.getenv('KOMMO_CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': os.getenv('REFRESH_TOKEN')
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=data, headers=headers)
    res.raise_for_status()
    return res.json()['access_token']

def gerar_callback(request):
    code = request.query_params.get('code')
    if not code:
        return {'erro': 'Nenhum código recebido'}

    token_url = f'{os.getenv('KOMMO_URL')}/oauth2/access_token'
    payload = {
        'client_id': os.getenv('KOMMO_CLIENT_ID'),
        'client_secret': os.getenv('KOMMO_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('KOMMO_REDIRECT_URI')
    }

    res = requests.post(token_url, data=payload)
    data = res.json()

    if 'access_token' in data:
        with open('../.env', 'a') as f:
            f.write(f'KOMMO_FOREVER_TOKEN={data['access_token']}')
        return {'status': 'ok', 'tokens': data}
    else:
        return {'erro': 'Não foi possível gerar o token', 'detalhe': data}
