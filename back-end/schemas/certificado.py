from pydantic import BaseModel
from datetime import datetime


class CertificadoSchema(BaseModel):
    """ Define como um novo certificado a ser inserido deve ser representado
    """
    tag_medidor: str = "FQI-101001"
    id_certificado: str = "CERT-SGMPBR001"
    data_calibracao: datetime = datetime.now()


