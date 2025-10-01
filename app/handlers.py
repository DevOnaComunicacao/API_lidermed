from fastapi.responses import JSONResponse
from app.send import enviar_lidermedtech, enviar_lidermed

def handler_lidermedtech(interessados):

    if interessados.nome == "":
        return JSONResponse(content={"erro": "insira um nome"})
    if interessados.empresa == "":
        return JSONResponse(content={"erro": "insira uma empresa"})
    if interessados.cnpj == "":
        return JSONResponse(content={"erro": "insira um cnpj válido"})
    if interessados.cargo == "":
        return JSONResponse(content={"erro": "insira um cargo"})
    if interessados.email == "":
        return JSONResponse(content={"erro": "insira um email válido"})
    if interessados.whatsapp == "":
        return JSONResponse(content={"erro": "insira um whatsapp válido"})
    if interessados.interesse != "sim" and interessados.interesse != "não":
        return JSONResponse(content={"erro: campo inválido"})
    if interessados.origem == "":
        return JSONResponse(content={"erro": "origem inválida"})
    if interessados.utm_source == "":
        return JSONResponse(content={"erro": "utm inválida"})
    if interessados.data_hora == "":
        return JSONResponse(content={"erro": "data inválida"})

    interessados.nome = interessados.nome.title()
    interessados.empresa = interessados.empresa.title()
    interessados.cargo = interessados.cargo.title()
    interessados.origem = interessados.origem.title()
    interessados.utm_source = interessados.utm_source.title()

    return enviar_lidermedtech(interessados)

def handler_lidermed(compradores):
    if compradores.nome == "":
        return JSONResponse(content={"erro": "insira um nome"})
    if compradores.whatsapp == "":
        return JSONResponse(content={"erro": "insira um whatsapp válido"})
    if compradores.email == "":
        return JSONResponse(content={"erro": "insira um email válido"})

    compradores.nome = compradores.nome.title()

    return enviar_lidermed(compradores)
