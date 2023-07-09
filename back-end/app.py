import flask
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Medidor, Certificado
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API - Sistema de Gestão de Medição de O&G", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
medidor_tag = Tag(name="Medidor", description="Cadastro, consulta e remoção de produtos à base")
certificado_tag = Tag(name="Certificado", description="Adição de um certificado à um medidor")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/medidor', tags=[medidor_tag],
          responses={"200": MedidorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: MedidorSchema):
    """Adiciona um novo Medidor à base de dados

    Retorna uma representação dos medidores e certificados associados.
    """
    medidor = Medidor(
        tag = form.tag, 
        descricao = form.descricao, 
        codigo_instalacao = form.codigo_instalacao)

    logger.debug(f"Adicionando medidor com a tag: '{medidor.tag}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(medidor)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado medidor tag: '{medidor.tag}'")
        return apresenta_medidor(medidor), 200

    except IntegrityError as e:
        # como a duplicidade da tag é a provável razão do IntegrityError
        error_msg = "Medidor de mesma tag já salvo na base :/"
        logger.warning(f"Erro ao adicionar medidor '{medidor.tag}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar medidor '{medidor.tag}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/medidores', tags=[medidor_tag],
         responses={"200": ListagemMedidoresSchema, "404": ErrorSchema})
def get_medidores():
    """Faz a busca por todos os Medidores cadastrados

    Retorna uma representação da listagem de medidores.
    """
    logger.debug(f"Buscando medidores ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    medidores = session.query(Medidor).all()

    if not medidores:
        # se não há produtos cadastrados
        return {"medidores": []}, 200
    else:
        logger.debug(f"%d medidores econtrados" % len(medidores))
        # retorna a representação de produto
        print(medidores)
        return apresenta_medidores(medidores), 200


@app.delete('/medidor', tags=[medidor_tag],
            responses={"200": MedidorDelSchema, "404": ErrorSchema})
def del_produto(query: MedidorBuscaSchema):

    """Deleta um Medidor a partir da tag informada

    Retorna uma mensagem de confirmação da remoção.
    """
    medidor = unquote(unquote(query.tag))
    print(medidor)
    logger.debug(f"Deletando dados sobre produto #{medidor}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Medidor).filter(Medidor.tag == medidor).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{medidor}")
        return {"mesage": "Produto removido", "id": medidor}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{medidor}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.get('/medidor', tags=[medidor_tag],
         responses={"200": MedidorViewSchema, "404": ErrorSchema})
def get_medidor(query: MedidorBuscaSchema):
    """Faz a busca por um Medidor a partir da tag do medidor

    Retorna o medidor e os certificados associados a ele.
    """
    medidor_id = query.tag
    logger.debug(f"Coletando dados sobre o medidor #{medidor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    medidor = session.query(Medidor).filter(Medidor.tag == medidor_id).first()

    if not medidor:
        # se o produto não foi encontrado
        error_msg = "Medidor não encontrado na base :/"
        logger.warning(f"Erro ao buscar medidor '{medidor_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Medidor econtrado: '{medidor.tag}'")
        # retorna a representação de produto
        return apresenta_medidor(medidor), 200

@app.post('/certificado', tags=[certificado_tag],
          responses={"200": MedidorViewSchema, "404": ErrorSchema})
def add_certificado(form: CertificadoSchema):
    """Adiciona de um novo certificado a um medidor identificado pela tag

    Retorna uma representação dos medidores com a lista de certificados associados.
    """
    medidor_id  = form.tag_medidor
    logger.debug(f"Adicionando certificado ao medidor #{medidor_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo produto
    medidor = session.query(Medidor).filter(Medidor.tag == medidor_id).first()

    if not medidor:
        # se produto não encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao adicionar certificado ao produto '{medidor}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o certificado
    id_certificado = form.id_certificado
    data_calibracao = form.data_calibracao
    certificado = Certificado(id_certificado, data_calibracao)
    medidor.adiciona_certificado(certificado)

    # adicionando o comentário ao produto
    session.commit()

    logger.debug(f"Adicionado certificado ao medidor #{medidor}")

    # retorna a representação de produto
    return apresenta_medidor(medidor), 200
