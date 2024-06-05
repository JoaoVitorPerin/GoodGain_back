from django.http import JsonResponse

import BO.cliente.cliente
import BO.integracao.sportradar
import BO.esporte.esporte
from rest_framework.views import APIView


class AlterarsenhaView(APIView):
    def post(self,*args, **kwargs):
        cpf = self.request.data.get('cpf')
        password = self.request.data.get('password')
        old_password = self.request.data.get('oldPassword')
        status, mensagem = BO.cliente.cliente.Cliente(password=password).alterar_senha(cpf=cpf, old_password=old_password)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class ResetSenhaView(APIView):
    def post(self,*args, **kwargs):
        email = self.request.data.get('email')
        status, mensagem, cliente = BO.cliente.cliente.Cliente().resetar_senha(email=email)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class Campeonato(APIView):

    def get(self, *args, **kwargs):
        status, dados = BO.esporte.esporte.Esporte().get_campeonatos()
        return JsonResponse({'status': status, 'campeonatos': dados})

class SimularAposta(APIView):

    def post(self, *args, **kwargs):
        cpf_user = self.request.GET.get('cpf_user')
        campeonato = self.request.GET.get('campeonato')
        time_1 = self.request.GET.get('time_1')
        time_2 = self.request.GET.get('time_2')
        odd = self.request.GET.get('odd')
        tipo_aposta = self.request.GET.get('tipo_aposta')
        status, dados = BO.cliente.cliente.Cliente().simular_aposta(cpf_user=cpf_user,
                                                                    campeonato=campeonato,
                                                                    time_1=time_1,
                                                                    time_2=time_2,
                                                                    odd=odd,
                                                                    tipo_aposta=tipo_aposta)
        return JsonResponse({'status': status, 'campeonatos': dados})

class EventoSimulado(APIView):

    def post(self, *args, **kwargs):
        cpf_user = self.request.GET.get('cpf_user')
        evento = self.request.GET.get('evento')
        status, dados = BO.cliente.cliente.Cliente().evento_simulado(cpf_user=cpf_user, evento=evento)
        return JsonResponse({'status': status, 'campeonatos': dados})
class Dashboard(APIView):

    def get(self, *args, **kwargs):
        cpf_user = self.request.GET.get('cpf_user')
        status, dados = BO.cliente.cliente.Cliente().get_dahsboard_cliente(cliente_id=cpf_user)
        return JsonResponse({'status': status, 'campeonatos': dados})


class GetCampeonatosTImes(APIView):

    def get(self, *args, **kwargs):
        campeonato_id = self.request.GET.get('campeonato_id')
        status, dados = BO.esporte.esporte.Esporte().get_times_campeonato(campeonato_id=campeonato_id)
        return JsonResponse({'status': status, 'times': dados})

class VerficarCodigo(APIView):

    def get(self, *args, **kwargs):
        email = self.request.GET.get('email')
        status, mensagem = BO.cliente.cliente.Cliente().gerar_codigo(email=email)
        return JsonResponse({'status': status, 'mensagem': mensagem})
    def post(self,*args, **kwargs):
        email = self.request.data.get('email')
        codigo = self.request.data.get('codigo')
        password = self.request.data.get('password')
        status, mensagem = BO.cliente.cliente.Cliente(password=password).verificar_codigo(email=email, codigo=codigo)
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
        cpf = self.request.GET.get('cpf')
        status, mensagem = BO.cliente.cliente.Cliente().deletar_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class Preferencias(APIView):
    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        preferencia_user = BO.cliente.cliente.Cliente().get_preferencias_user(cpf=cpf)
        dados = BO.cliente.cliente.Cliente().get_preferencias()
        return JsonResponse({'preferencia_user': preferencia_user, 'dados': dados})

    def post(self, *args, **kwargs):
        esporte = self.request.data.get('esporte')
        opcoes_apostas = self.request.data.get('opcoes_apostas')
        cpf = self.request.data.get('cpf')


        status= BO.cliente.cliente.Cliente().cadastrar_preferencias(cpf=cpf,
                                                                          esporte=esporte,
                                                                          opcoes_apostas=opcoes_apostas
                                                                          )

        return JsonResponse({'status': status})

    # def put(self, *args, **kwargs):
    #     esporte = self.request.data.getlist('esporte')
    #     opcoes_apostas = self.request.data.getlist('opcoes_apostas')
    #     cpf = self.request.data.get('cpf')
    #
    #
    #     status= BO.cliente.cliente.Cliente().editar_preferencias(cpf=cpf,
    #                                                              esporte=esporte,
    #                                                              opcoes_apostas=opcoes_apostas
    #                                                              )
    #
    #     return JsonResponse({'status': status})

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

        status = BO.integracao.sportradar.Sportradar().atualizar_tudo()

        return JsonResponse({'status': status})