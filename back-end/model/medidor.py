from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base
from model.certificado import Certificado


class Medidor(Base):
    __tablename__ = 'medidor'

    id = Column("pk_medidor", Integer, primary_key=True)
    tag = Column(String(140), unique=True)
    descricao = Column(String(140))
    codigo_instalacao = Column(Integer)

    # Definição do relacionamento entre o medidor e o certificado.
    # Essa relação é implicita, não está salva na tabela 'medidor',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    certificados = relationship("Certificado")

    def __init__(self, tag:str, descricao:str, codigo_instalacao:int):
        """
        Cria um Medidor

        Arguments:
            tag: tag do medidor.
            descricao: descrição breve do medidor
            codigo_instalacao: código da instalação onde o medidor opera
        """
        self.tag = tag
        self.descricao = descricao
        self.codigo_instalacao = codigo_instalacao

    def adiciona_certificado(self, certificado:Certificado):
        """ Adiciona um novo comentário ao Produto
        """
        self.certificados.append(certificado)

