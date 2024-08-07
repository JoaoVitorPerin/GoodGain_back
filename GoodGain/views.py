from django.http import JsonResponse

import BO.cliente.cliente
import BO.integracao.sportradar
import BO.integracao.apifootball
import BO.esporte.esporte
from rest_framework.views import APIView
from BO.autenticacao.autenticacao import validar_perfil
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response
import datetime

from rest_framework_simplejwt.views import TokenObtainPairView
from BO.cliente.cliente import MyTokenObtainPairSerializer  # Certifique-se de importar corretamente seu serializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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
        cpf_user = self.request.POST.get('cpf_user')
        campeonato = self.request.POST.get('campeonato')
        time_1 = self.request.POST.get('time1')
        time_2 = self.request.POST.get('time2')
        odd = self.request.POST.get('odd')
        tipo_aposta = self.request.POST.get('tipoAposta')
        valor = self.request.POST.get('valor')
        is_aposta = self.request.POST.get('is_aposta')
        casa_aposta = self.request.POST.get('casa_aposta')
        dados = BO.cliente.cliente.Cliente().simular_aposta(cpf_user=cpf_user,
                                                                    campeonato=campeonato,
                                                                    time_1=time_1,
                                                                    time_2=time_2,
                                                                    odd=odd,
                                                                    tipo_aposta=tipo_aposta,
                                                                    valor=valor,
                                                                    is_aposta=is_aposta,
                                                                    casa_aposta=casa_aposta)
        return JsonResponse(dados)

class EventoSimulado(APIView):

    def post(self, *args, **kwargs):
        cpf_user = self.request.GET.get('cpf_user')
        evento = self.request.GET.get('evento')
        status, dados = BO.cliente.cliente.Cliente().evento_simulado(cpf_user=cpf_user, evento=evento)
        return JsonResponse({'status': status, 'campeonatos': dados})
class Dashboard(APIView):

    def get(self, *args, **kwargs):
        if validar_perfil(user=self.request.user, nivel_necessario=2):
            cpf_user = self.request.GET.get('cpf_user')
            dados, lista_tipos, lista_campeonatos = BO.cliente.cliente.Cliente().get_dahsboard_cliente(cliente_id=cpf_user)
            return JsonResponse({'dados': dados, 'tipos':lista_tipos, 'campeonatos': lista_campeonatos})

class EventosFuturos(APIView):

    def get(self, *args, **kwargs):
        status, dados = BO.esporte.esporte.Esporte().get_eventos()

        return JsonResponse({'status':True,'dados': dados})

class EventosRecomendados(APIView):

    def get(self, *args, **kwargs):
        status, dados = BO.esporte.esporte.Esporte().get_eventos_recomendados(cliente=self.request.user)

        return JsonResponse({'status':True,'dados': dados})


class Historico(APIView):

    def get(self, *args, **kwargs):
        cpf_user = self.request.GET.get('cpf_user')
        status, lista_apostas_cliente = BO.cliente.cliente.Cliente().get_apostas_cliente(cpf_user=cpf_user)
        return JsonResponse({'status': status, 'lista_apostas_cliente': lista_apostas_cliente})


class ValidarPerfil(APIView):

    def get(self, *args, **kwargs):

        status, descricao = validar_perfil(user=self.request.user,nivel_necessario=2)
        return JsonResponse({'status': status, 'descricao': descricao})



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

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def minha_view(request):
#     # Sua lógica de negócio aqui
#     return Response({"mensagem": "Esta é uma página acessível sem autenticação."})
class Cliente(APIView):

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
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

        return JsonResponse({'status': status, 'descricao':mensagem})

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
        valor = self.request.data.get('stack_aposta')


        status= BO.cliente.cliente.Cliente().cadastrar_preferencias(cpf=cpf,
                                                                          esporte=esporte,
                                                                          opcoes_apostas=opcoes_apostas,
                                                                          valor=valor
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
        data = self.request.GET.get('data')
        dados = BO.integracao.apifootball.Apifootball().atualizar_base(data=data)

        return JsonResponse({'status': dados})

class ListarUsarios(APIView):
    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        username = self.request.GET.get('username')
        dados = BO.cliente.cliente.Cliente(username=username).get_todos_usuarios(cpf_cliente=cpf)

        return JsonResponse({'dados': dados})

class ListarLogs(APIView):
    def get(self, *args, **kwargs):
        operacao = self.request.GET.get('operacao')
        dados = BO.esporte.esporte.Esporte().get_log(operacao=operacao)

        return JsonResponse({'dados': dados})

class ListaOperacoes(APIView):
    def get(self, *args, **kwargs):
        dados = BO.esporte.esporte.Esporte().get_operacoes()

        return JsonResponse({'dados': dados})

class ListaPerfis(APIView):
    def get(self, *args, **kwargs):
        dados = BO.cliente.cliente.Cliente().get_perfis()

        return JsonResponse({'dados': dados})


class EditarUsuarioAdmin(APIView):
    def put(self, *args, **kwargs):
        if self.request.user.perfil.nivel == 0:
            username = self.request.data.get('username')
            password = self.request.data.get('password')
            nome = self.request.data.get('nome')
            sobrenome = self.request.data.get('sobrenome')
            email = self.request.data.get('email')
            cpf = self.request.data.get('cpf')
            data_nasc = self.request.data.get('data_nascimento')
            perfil = self.request.data.get('perfil')

            status, mensagem = BO.cliente.cliente.Cliente(username=username, password=password).editar_cliente(nome=nome,
                                                                                                               sobrenome=sobrenome,
                                                                                                               email=email,
                                                                                                               cpf=cpf,
                                                                                                               data_nasc=data_nasc,
                                                                                                               perfil=perfil)
        else:
            status, mensagem = False, 'essa conta não tem nivel de acesso o suficiente para editar'
        return JsonResponse({'status': status, 'mensagem': mensagem})