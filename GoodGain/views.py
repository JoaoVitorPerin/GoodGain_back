from django.http import JsonResponse

import BO.cliente.cliente
import BO.integracao.sportradar
from rest_framework.views import APIView


class AlterarsenhaView(APIView):
    def post(self,*args, **kwargs):
        cpf = self.request.data.get('cpf')
        password = self.request.data.get('password')
        status, mensagem, cliente = BO.cliente.cliente.Cliente(password=password).alterar_senha(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class ResetSenhaView(APIView):
    def post(self,*args, **kwargs):
        email = self.request.data.get('email')
        status, mensagem, cliente = BO.cliente.cliente.Cliente().resetar_senha(email=email)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class VerficarCodigo(APIView):

    def get(self, *args, **kwargs):
        email = self.request.GET.get('email')
        status, mensagem, cliente = BO.cliente.cliente.Cliente().get_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem, 'cliente': cliente})
    def post(self,*args, **kwargs):
        email = self.request.data.get('email')
        codigo = self.request.data.get('codigo')
        status, mensagem, cliente = BO.cliente.cliente.Cliente().resetar_senha(email=email)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class Cliente(APIView):
    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        status, mensagem, cliente = BO.cliente.cliente.Cliente().get_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem, 'cliente': cliente})

    def post(self, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        nome = self.request.data.get('nome')
        sobrenome = self.request.data.get('sobrenome')
        email = self.request.data.get('email')
        cpf = self.request.data.get('cpf')
        data_nasc = self.request.data.get('dataNascimento')

        status, mensagem = BO.cliente.cliente.Cliente(username=username, password=password).cadastrar_cliente(nome=nome,
                                                                                                              sobrenome=sobrenome,
                                                                                                              email=email,
                                                                                                              cpf=cpf,
                                                                                                              data_nasc=data_nasc)

        return JsonResponse({'status': status})

    def put(self, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        nome = self.request.data.get('nome')
        sobrenome = self.request.data.get('sobrenome')
        email = self.request.data.get('email')
        cpf = self.request.data.get('cpf')
        data_nasc = self.request.data.get('data_nascimento')

        status, mensagem = BO.cliente.cliente.Cliente(username=username, password=password).editar_cliente(nome=nome,
                                                                                                           sobrenome=sobrenome,
                                                                                                           email=email,
                                                                                                           cpf=cpf,
                                                                                                           data_nasc=data_nasc)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def delete(self, *args, **kwargs):
        cpf = self.request.data.get('cpf')
        status, mensagem = BO.cliente.cliente.Cliente().deletar_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class Preferencias(APIView):
    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        preferencia_user = BO.cliente.cliente.Cliente().get_preferencias_user(cpf=cpf)
        dados, = BO.cliente.cliente.Cliente().get_preferencias()
        return JsonResponse({'preferencia_user': preferencia_user, 'dados': dados})

    def post(self, *args, **kwargs):
        esporte = self.request.data.getlist('esporte')
        opcoes_apostas = self.request.data.getlist('opcoes_apostas')
        cpf = self.request.data.get('cpf')


        status= BO.cliente.cliente.Cliente().cadastrar_preferencias(cpf=cpf,
                                                                          esporte=esporte,
                                                                          opcoes_apostas=opcoes_apostas
                                                                          )

        return JsonResponse({'status': status})

    def put(self, *args, **kwargs):
        esporte = self.request.data.getlist('esporte')
        opcoes_apostas = self.request.data.getlist('opcoes_apostas')
        cpf = self.request.data.get('cpf')


        status= BO.cliente.cliente.Cliente().editar_preferencias(cpf=cpf,
                                                                 esporte=esporte,
                                                                 opcoes_apostas=opcoes_apostas
                                                                 )

        return JsonResponse({'status': status})

class Login(APIView):
    def get(self, *args, **kwargs):
        return

    def post(self, *args, **kwargs):
        user = self.request.data.get('username')
        password = self.request.data.get('password')

        status, descricao, token_jwt = BO.cliente.cliente.Cliente(username=user, password=password).logar()

        return JsonResponse({'status': status,'descricao': descricao,'token': token_jwt})










#classes do Admin

class PegarVersusu(APIView):
    def get(self, *args, **kwargs):

        status = BO.integracao.sportradar.Sportradar().pegar_versus_futebol()

        return JsonResponse({'status': status})

class AtualizarDados(APIView):
    def get(self, *args, **kwargs):

        status = BO.integracao.sportradar.Sportradar().atualizar_dados()

        return JsonResponse({'status': status})