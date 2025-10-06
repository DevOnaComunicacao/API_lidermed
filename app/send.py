from fastapi.responses import JSONResponse
import requests
import dotenv
import os
from app.auth import criar_token_kommo
from pathlib import Path

if os.getenv("RENDER") != "true":
    env_path = Path(__file__).parent / ".env"
    dotenv.load_dotenv(dotenv_path=env_path)
    print("Carregando .env localmente")
else:
    print("Rodando no Render, .env ignorado")

url = os.getenv('KOMMO_URL')

def enviar_lidermedtech(interessados):

    token = criar_token_kommo()

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        # Lead
        lead_payload = [{
            'name': interessados.nome,
            'custom_fields_values': [
                {
                    "field_id": 1066712,  # ID do campo Empresa
                    "values": [{"value": interessados.empresa}]
                },
                {
                    "field_id": 1070092,  # ID do campo CNPJ
                    "values": [{"value": interessados.cnpj}]
                },
                {
                    "field_id": 1104100,  # ID do campo Origem
                    "values": [{"value": interessados.origem}]
                },
                {
                    "field_id": 1104102,  # ID do campo Utm
                    "values": [{"value": interessados.utm_source}]
                }
            ]
        }]
        lead_res = requests.post(f'{url}/api/v4/leads', json=lead_payload, headers=headers)

        if lead_res.status_code not in (200, 201):
            return {
                'ok': False,
                'step': 'lead',
                'status': lead_res.status_code,
                'error': lead_res.text
            }

        lead_id = lead_res.json()['_embedded']['leads'][0]['id']

        contact_payload = [{
            'name': interessados.nome,
            'custom_fields_values': [
                {'field_code': 'EMAIL', 'values': [{'value': interessados.email}]},
                {'field_code': 'PHONE', 'values': [{'value': interessados.whatsapp}]}
            ]
        }]
        contact_res = requests.post(f'{url}/api/v4/contacts', json=contact_payload, headers=headers)

        if contact_res.status_code not in (200, 201):
            return {
                'ok': False,
                'step': 'contact',
                'status': contact_res.status_code,
                'error': contact_res.text
            }

        contact_id = contact_res.json()['_embedded']['contacts'][0]['id']

        # Linkar contato ao lead
        link_payload = [{'to_entity_id': contact_id, 'to_entity_type': 'contacts'}]
        link_res = requests.post(f'{url}/api/v4/leads/{lead_id}/link', json=link_payload, headers=headers)

        if link_res.status_code in (200, 201):
            return JSONResponse(content={'status': 'dados enviados com sucesso!'})

        return {
            'ok': False,
            'step': 'link',
            'status': link_res.status_code,
            'error': link_res.text
        }

    except Exception as e:
        return JSONResponse(content={'erro': f'{e}'})

def enviar_lidermed(compradores):
    token = criar_token_kommo()
    origem = "Lídermed"

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    try:
        # Lead
        lead_payload = [{
            'name': compradores.nome,
            'custom_fields_values': [
                {
                    "field_id": 1104100,  # ID do campo Origem
                    "values": [{"value": origem}]
                }
            ]
        }]
        lead_res = requests.post(f'{url}/api/v4/leads', json=lead_payload, headers=headers)

        if lead_res.status_code not in (200, 201):
            return {
                'ok': False,
                'step': 'lead',
                'status': lead_res.status_code,
                'error': lead_res.text
            }

        lead_id = lead_res.json()['_embedded']['leads'][0]['id']

        contact_payload = [{
            'name': compradores.nome,
            'custom_fields_values': [
                {'field_code': 'EMAIL', 'values': [{'value': compradores.email}]},
                {'field_code': 'PHONE', 'values': [{'value': compradores.whatsapp}]}
            ]
        }]
        contact_res = requests.post(f'{url}/api/v4/contacts', json=contact_payload, headers=headers)

        if contact_res.status_code not in (200, 201):
            return {
                'ok': False,
                'step': 'contact',
                'status': contact_res.status_code,
                'error': contact_res.text
            }

        contact_id = contact_res.json()['_embedded']['contacts'][0]['id']

        # Linkar contato ao lead
        link_payload = [{'to_entity_id': contact_id, 'to_entity_type': 'contacts'}]
        link_res = requests.post(f'{url}/api/v4/leads/{lead_id}/link', json=link_payload, headers=headers)

        if link_res.status_code in (200, 201):
            return JSONResponse(content={'status': 'dados enviados com sucesso!'})

        return {
            'ok': False,
            'step': 'link',
            'status': link_res.status_code,
            'error': link_res.text
        }

    except Exception as e:
        return JSONResponse(content={'erro': f'{e}'})








