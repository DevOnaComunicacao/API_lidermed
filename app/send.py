from fastapi.responses import JSONResponse
import requests
import dotenv
import os

dotenv.load_dotenv()

url = "https://lidermed.kommo.com"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImVhMzdkMTQ5ZDIxYjkxNWQ3MTBlZDRlNGU0MjkyZDk0MWQ4OThhNzdhZTU1MmQ3MzgzOWU2MjRlNGY4NzQ4MTJjOTg1Y2U2MDgyNzcyYTA3In0.eyJhdWQiOiI2MzA0N2ZmNi1kNDMyLTQ2ZGYtYWRkOS0wMTEyNDYzNTg2NjAiLCJqdGkiOiJlYTM3ZDE0OWQyMWI5MTVkNzEwZWQ0ZTRlNDI5MmQ5NDFkODk4YTc3YWU1NTJkNzM4MzllNjI0ZTRmODc0ODEyYzk4NWNlNjA4Mjc3MmEwNyIsImlhdCI6MTc1ODE5Nzg5MywibmJmIjoxNzU4MTk3ODkzLCJleHAiOjE5MTU5MjAwMDAsInN1YiI6IjEyODE3MTk1IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjM0MjYwMTYzLCJiYXNlX2RvbWFpbiI6ImtvbW1vLmNvbSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwidXNlcl9mbGFncyI6MCwiaGFzaF91dWlkIjoiY2U2NjU3NTctOTMzYS00OWQwLWI5MDgtZWVjYjBiMTFlMWRhIiwiYXBpX2RvbWFpbiI6ImFwaS1jLmtvbW1vLmNvbSJ9.h19U9EwQQH1cDLJNSAVgflj5ZQ9czMBIjm1ZoaP9L7UN_0Y1bgifsdd1dQAYy0xo9uOe29EtgMVbioDkOld2Pyycy3_BtDWaMu5v6T60-DLcAL8KiyqBK42WiAADs4VM1yovpWa9P4P1w-DCVaTQQAmnDRAqrsJ0ofXaNrzHV2qQUYSVTf53rGLWxtk95OxL28oDjN410UCq-TzUCXTAiPcBuCcGNy68QlHUiZ4wWidr5hFEmAtll0rzSDa1nqQ5IkA2WX4dMrm3ZayzNzdW0P7QnZi8W-Bv9oWsz7FKcTv0S7h_2mwEZlgzYslfzelgNpt0O0LcHf2JCXRwUFb9QA"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

def enviar_lidermedtech(interessados):
    try:
        lead_payload = [{"name": interessados.nome}]
        lead_res = requests.post(f"{url}/api/v4/leads", json=lead_payload, headers=headers)

        if lead_res.status_code not in (200, 201):
            return {"ok": False, "step": "lead", "status": lead_res.status_code, "error": lead_res.text}

        #if lead_res.status_code not in (200, 201):
         #   return JSONResponse(
          #      content={"erro": "Falha ao criar lead", "detalhe": lead_res.text},
          #      status_code=lead_res.status_code
          #  )

        lead_id = lead_res.json()["_embedded"]["leads"][0]["id"]

        contact_payload = [{
        "name": interessados.nome,
        "custom_fields_values": [
            {"field_code": "EMAIL", "values": [{"value": interessados.email}]},
            {"field_code": "PHONE", "values": [{"value": interessados.whatsapp}]},
            ]
        }]
        contact_res = requests.post(f"{url}/api/v4/contacts", json=contact_payload, headers=headers)

        contact_id = contact_res.json()["_embedded"]["contacts"][0]["id"]

        link_payload = [{"to_entity_id": contact_id, "to_entity_type": "contacts"}]
        link_res = requests.post(f"{url}/api/v4/leads/{lead_id}/link", json=link_payload, headers=headers)

        if link_res.status_code in (200, 201):
            return JSONResponse(content={"status": "dados enviados com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"erro": f"{e}"})


def enviar_lidermed(compradores):
    print(compradores)

    return JSONResponse(content={"status": "enviado com sucesso!"})

