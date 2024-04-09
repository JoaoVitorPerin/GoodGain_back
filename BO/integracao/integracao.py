import unicodedata
from decimal import Decimal

import requests
import json
from django.apps import apps


# import core.sistema.models
# import core.produto.models
import http.client
import xmltodict
# import util.TratarCampos


class Integracao:

    def __init__(self, url=None, body=None, headers=None, servico=None, request=None):
        self.url = url
        self.body = body
        self.headers = headers
        self.response = None
        self.response_text = None
        self.servico = servico
        self.status_code = None
        self.tipo = None
        self.cert = None
        self.request = request
        http.client._MAXHEADERS = 1000

    # def salvar(self):
    #
    #     try:
    #         log_model = apps.get_model('log', BANCO.capitalize() + 'Integracao')
    #
    #         nova_integracao = log_model(
    #             servico=self.servico,
    #             url=self.url,
    #             body=self.body,
    #             headers=self.headers,
    #             response=self.response,
    #             status_code=self.status_code,
    #             tipo=self.tipo
    #         )
    #         nova_integracao.save(request_=self.request, using='log')
    #         return True
    #     except:
    #         return False

    def tratar_campo(self, campo=None):

        if isinstance(campo, str) and campo is not None:
            campo = unicodedata.normalize('NFD', campo)

        if isinstance(campo, Decimal):
            campo = float(campo)

        return campo if campo is not None else ''

    def post(self, dumps=True, unicode=True, auth=None, json_content=False, arquivos=None, parametros=None, ensure_ascii=False, timeout=15, verify=True):


        data = self.body
        if dumps:
            data = json.dumps(data, ensure_ascii=ensure_ascii)
        if unicode and isinstance(data, str):
            data = unicodedata.normalize('NFD', data).encode('ASCII', 'ignore')

        if not json_content:
            resposta = requests.post(self.url, data=data, headers=self.headers, files=arquivos, params=parametros, auth=auth, timeout=timeout, verify=verify, cert=self.cert)
        else:
            resposta = requests.post(self.url, json=data, headers=self.headers, files=arquivos, params=parametros, auth=auth, timeout=timeout, verify=verify, cert=self.cert)
        self.response = resposta.content
        self.status_code = resposta.status_code
        # self.salvar()

    def get(self, dumps=False, auth=None, parametros=None, verify=True):


        data = self.body
        if dumps:
            data = json.dumps(data)

        resposta = requests.get(self.url, headers=self.headers, data=data, auth=auth, params=parametros, verify=verify)
        self.response = resposta.content
        self.response_text = resposta.text
        self.status_code = resposta.status_code
        # self.salvar()

    def delete(self):
        resposta = requests.delete(self.url, headers=self.headers, data=self.body)
        self.response = resposta.content
        self.status_code = resposta.status_code
        # self.salvar()

    def put(self, dumps=False, unicode=True, ensure_ascii=False, arquivos=None):
        data = self.body
        if dumps:
            data = json.dumps(data, ensure_ascii=ensure_ascii)

        resposta = requests.put(self.url, headers=self.headers, data=data, files=arquivos)
        self.response = resposta.content
        self.status_code = resposta.status_code
        # self.salvar()

    def options(self):
        resposta = requests.options(self.url, headers=self.headers, data=self.body)
        self.response = resposta.content
        self.status_code = resposta.status_code
        # self.salvar()

    def head(self):
        resposta = requests.head(self.url, headers=self.headers, data=self.body)
        self.response = resposta.content
        self.status_code = resposta.status_code
        # self.salvar()

    def patch(self, dumps=True, unicode=True, ensure_ascii=False):
        data = self.body
        if dumps:
            data = json.dumps(data, ensure_ascii=ensure_ascii)
        if unicode and isinstance(data, str):
            data = unicodedata.normalize('NFD', data).encode('ASCII', 'ignore')

        resposta = requests.patch(url=self.url, headers=self.headers, data=data)

        self.response = resposta.content
        self.status_code = resposta.status_code
        # self.salvar()

    def salvar_webhook(self, body=None, status_code=None, headers=None, response=None):
        self.body = body
        self.status_code = status_code
        self.headers = headers
        self.response = response
        # self.salvar()

    def converter_resposta_xml_para_json(self):
        self.response = xmltodict.parse(self.response)

    def carregar_chaves(self):
        pass

    def fazer_request(self, tipo, url, request_tipo, body=None, is_tratar_response=True, response_tipo='JSON', **parametros):
        self.tipo = tipo
        self.url = url
        self.body = body

        request_tipo = request_tipo.upper()

        if request_tipo == 'POST':
            self.post(**parametros)
        elif request_tipo == 'GET':
            self.get(**parametros)
        elif request_tipo == 'PUT':
            self.put()
        elif request_tipo == 'PATCH':
            self.patch(**parametros)
        elif request_tipo == 'DELETE':
            self.delete()
        else:
            return False

        if is_tratar_response:
            self.tratar_response(response_tipo=response_tipo)

        return True

    def tratar_response(self, response_tipo='JSON'):
        try:
            response_tipo = response_tipo.upper()

            if response_tipo == 'JSON':
                self.response = json.loads(self.response)
            elif response_tipo == 'XML':
                self.response = xmltodict.parse(self.response)
            elif response_tipo == 'TEXT':
                self.response = self.response.decode('utf-8')  # str(self.response)
            elif response_tipo == 'BYTES':
                pass
            else:
                return False

        except Exception as e:
            return False

        return True

    def is_status_code_valido(self):
        if self.status_code in [100, 200, 201, 202, 302]:
            return True
        return False

    def salvar_log_feed(self, lista_produtos=[], status=True):
        try:
            if self.servico == 'google':
                servico = 'google_shop'
            else:
                servico = self.servico
            #
            # feed = core.produto.models.Feed.objects.get(nome=servico)
            # core.produto.models.ProdutoFeedLog(
            #     feed_id=feed.id,
            #     qtd_produtos=len(lista_produtos),
            #     json_produtos=json.dumps(lista_produtos),
            #     status=status
            # ).save()
            return True
        except:
            return False

    def carregar_chaves(self):
        pass

    def fazer_request(self, tipo, url, request_tipo, body=None, is_tratar_response=True, response_tipo='JSON', **parametros):
        self.tipo = tipo
        self.url = url
        self.body = body

        request_tipo = request_tipo.upper()

        if request_tipo == 'POST':
            self.post(**parametros)
        elif request_tipo == 'GET':
            self.get(**parametros)
        elif request_tipo == 'PUT':
            self.put()
        elif request_tipo == 'PATCH':
            self.patch(**parametros)
        elif request_tipo == 'DELETE':
            self.delete()
        else:
            return False

        if is_tratar_response:
            self.tratar_response(response_tipo=response_tipo)

        return True

    def tratar_response(self, response_tipo='JSON'):
        try:
            response_tipo = response_tipo.upper()

            if response_tipo == 'JSON':
                self.response = json.loads(self.response)
            elif response_tipo == 'XML':
                self.response = xmltodict.parse(self.response)
            elif response_tipo == 'TEXT':
                self.response = self.response.decode('utf-8')  # str(self.response)
            elif response_tipo == 'BYTES':
                pass
            else:
                return False

        except Exception as e:
            return False

        return True

    def is_status_code_valido(self):
        if self.status_code in [100, 200, 201, 202, 302]:
            return True
        return False

    # def verificar_integracoes(self):
    #     urls = core.sistema.models.ChavesIntegracao.objects.ativos().values_list('url', flat=True)
    #     urls = list(set(urls))
    #
    #     lista_ativos = []
    #     lista_inativos = []
    #     lista_codigo_erro = []
    #
    #     self.tipo = 'verificar_integracoes'
    #     for url in urls:
    #         try:
    #             self.url = url
    #             self.head()
    #             if self.status_code == 200:
    #                 # print(f"URL {url} is active.")
    #                 lista_ativos.append(url)
    #             elif util.TratarCampos.is_url_local(url=url):
    #                 # print(f"URL {url} is private.")
    #                 lista_ativos.append(url)
    #             else:
    #                 # print(f"URL {url} returned a status code: {self.status_code}")
    #                 lista_codigo_erro.append(url)
    #         except Exception as e:
    #             # print(f"Could not connect to URL: {url}")
    #             lista_inativos.append(url)
    #
    #     # print(f'Ativos: {len(lista_ativos)} {lista_ativos}')
    #     # print(f'Inativos: {len(lista_inativos)} {lista_inativos}')
    #     # print(f'Codigos_erro: {len(lista_codigo_erro)} {lista_codigo_erro}')
    #
    #     #Update
    #     core.sistema.models.ChavesIntegracao.objects\
    #         .ativos()\
    #         .filter(url__in=lista_ativos+lista_codigo_erro)\
    #         .update(is_ativo=True)
    #
    #     core.sistema.models.ChavesIntegracao.objects\
    #         .ativos()\
    #         .filter(url__in=lista_inativos)\
    #         .update(is_ativo=False)

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @url.deleter
    def url(self):
        del self.__url

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, value):
        self.__body = value if value is not None else {}

    @body.deleter
    def body(self):
        del self.__body

    @property
    def headers(self):
        return self.__headers

    @headers.setter
    def headers(self, value):
        self.__headers = value if value is not None else {'Content-type': 'application/json'}

    @headers.deleter
    def headers(self):
        del self.__headers

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, value):
        self.__response = value

    @response.deleter
    def response(self):
        del self.__response

    @property
    def servico(self):
        return self.__servico

    @servico.setter
    def servico(self, value):
        self.__servico = value

    @servico.deleter
    def servico(self):
        del self.__servico

    @property
    def status_code(self):
        return self.__status_code

    @status_code.setter
    def status_code(self, value):
        self.__status_code = value

    @status_code.deleter
    def status_code(self):
        del self.__status_code

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, value):
        self.__tipo = value

    @tipo.deleter
    def tipo(self):
        del self.__tipo

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, value):
        self.__request = value

    @request.deleter
    def request(self):
        del self.__request


class Chave:
    def __init__(self, nome=None):
        self.nome = nome
        self.url = None
        self.usuario = None
        self.senha = None
        self.porta = None
        self.objeto = None
        self.carregar()

    # def carregar(self):
    #     try:
    #         if self.nome is not None:
    #             self.objeto = core.sistema.models.ChavesIntegracao.objects.ativos().all().filter(nome=self.nome).first()
    #             self.url = self.objeto.url
    #             self.usuario = self.objeto.usuario
    #             self.senha = self.objeto.senha
    #             self.porta = self.objeto.porta
    #         return self.objeto
    #     except:
    #         return self.objeto

    # def criar(self, nome=None, descricao=None, url=None, porta=None, usuario=None, senha=None, info_descricao=None, info_1=None, info_2=None, info_3=None, info_4=None, info_5=None):
    #     criar = core.sistema.models.ChavesIntegracao(nome=nome, descricao=descricao, url=url, porta=porta, usuario=usuario, senha=senha, info_descricao=info_descricao, info_1=info_1, info_2=info_2, info_3=info_3, info_4=info_4, info_5=info_5)
    #     criar.save()
    #     return criar

    def get(self, attr):
        if self.objeto is not None and hasattr(self.objeto, attr):
            return getattr(self.objeto, attr)
        else:
            return None
