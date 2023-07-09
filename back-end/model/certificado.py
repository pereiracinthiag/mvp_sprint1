from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model.base import Base


class Certificado(Base):
    __tablename__ = 'certificado'

    id = Column(Integer, primary_key=True)
    id_certificado = Column(String(4000))
    data_calibracao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o certificado e um medidor.
    # Aqui está sendo definido a coluna 'medidor' que vai guardar
    # a referencia ao certificado, a chave estrangeira que relaciona
    # um medidor ao certificado.
    medidor = Column(Integer, ForeignKey("medidor.pk_medidor"), nullable=False)

    def __init__(self, id_certificado:str, data_calibracao:Union[DateTime, None] = None):
        """
        Cria um Certificado

        Arguments:
            id_certificado: a identificação do certificado.
            data_calibração: data de quando o medidor foi calibrado. Esta data serve de base para programar as próximas
            calibrações.

        """
        self.id_certificado = id_certificado
        self.data_calibracao = data_calibracao
