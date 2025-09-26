from fastapi.responses import JSONResponse
import requests
import dotenv
import os
from app.auth import criar_token_kommo

dotenv.load_dotenv()

url = os.getenv('KOMMO_URL')
token = "a"
    #criar_token_kommo()

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

def enviar_lidermedtech(interessados):
    try:
        lead_payload = {'name': interessados.nome}
        lead_res = requests.post(f'{url}/api/v4/leads', json=lead_payload, headers=headers)

        if lead_res.status_code not in (200, 201):
            return {'ok': False, 'step': 'lead', 'status': lead_res.status_code, 'error': lead_res.text}

        lead_id = lead_res.json()['_embedded']['leads'][0]['id']

        contact_payload = [{
        'name': interessados.nome,
        'custom_fields_values': [
            {'field_code': 'EMAIL', 'values': [{'value': interessados.email}]},
            {'field_code': 'PHONE', 'values': [{'value': interessados.whatsapp}]},
            ]
        }]
        contact_res = requests.post(f'{url}/api/v4/contacts', json=contact_payload, headers=headers)

        contact_id = contact_res.json()['_embedded']['contacts'][0]['id']

        link_payload = [{'to_entity_id': contact_id, 'to_entity_type': 'contacts'}]
        link_res = requests.post(f'{url}/api/v4/leads/{lead_id}/link', json=link_payload, headers=headers)

        if link_res.status_code in (200, 201):
            return JSONResponse(content={'status': 'dados enviados com sucesso!'})
    except Exception as e:
        return JSONResponse(content={'erro': f'{e}'})


def enviar_lidermed(compradores):
    print(compradores)

    return JSONResponse(content={'status': 'enviado com sucesso!'})






