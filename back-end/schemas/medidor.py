from pydantic import BaseModel
from typing import Optional, List
from model.medidor import Medidor

from schemas import CertificadoSchema


class MedidorSchema(BaseModel):
    """ Define como um novo medidor a ser inserido deve ser representado
    """
    tag: str = "FQI-201001"
    descricao: str = "Medidor de fiscal de óleo"
    codigo_instalacao: int = 10121


class MedidorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na tag do medidor.
    """
    tag: str = "FQI-201001"


class ListagemMedidoresSchema(BaseModel):
    """ Define como uma listagem de medidores será retornada.
    """
    medidores:List[MedidorSchema]

class MedidorViewSchema(BaseModel):
    """ Define como um medidor será retornado: medidor + certificados.
    """
    id: int = 1
    tag: str = "FQI-201001"
    descricao:str = "Medidor de fiscal de óleo"
    total_certificados: int = 3
    certificados:List[CertificadoSchema]

class MedidorDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    tag: str

def apresenta_medidor(medidor: Medidor):
    """ Retorna uma representação do medidor seguindo o schema definido em
        MedidorViewSchema.
    """
    return {
        "id": medidor.id,
        "tag": medidor.tag,
        "descricao": medidor.descricao,
        "instalacao": medidor.codigo_instalacao,
        "total_certificados": len(medidor.certificados),
        "certificados": [{"id_certificado": c.id_certificado} for c in medidor.certificados]
    }


def apresenta_medidores(medidores: List[Medidor]):
    """ Retorna uma representação do medidor seguindo o schema definido em
        MedidorViewSchema.
    """
    result = []
    for medidor in medidores:
        result.append({
            "tag": medidor.tag,
            "descricao": medidor.descricao,
            "instalacao": medidor.codigo_instalacao,
        })

    return {"medidores": result}

