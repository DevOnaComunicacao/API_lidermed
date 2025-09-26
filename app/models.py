from pydantic import BaseModel

class Admin(BaseModel):
    usuario: str
    senha: str

class Interessados(BaseModel):
    nome: str
    empresa: str
    cnpj: str
    cargo: str
    email: str
    whatsapp: str
    interesse: str
    utm_source: str
    data_hora: str

class Compradores(BaseModel):
    nome: str
    empresa: str
    cnpj: str
    cargo: str
    email: str
    whatsapp: str
    compra: str
    utm_source: str
    data_hora: str