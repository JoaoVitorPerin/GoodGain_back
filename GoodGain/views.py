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
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """

        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get(self, *args, **kwargs):
        all_campeonatos = self.request.GET.get('all_campeonatos')
        status, dados = BO.esporte.esporte.Esporte().get_campeonatos(all_campeonatos)
        return JsonResponse({'status': status, 'campeonatos': dados})

    def post(self, *args, **kwargs):
        campeonato_id = self.request.data.get('campeonato_id')
        status, mensagem = BO.esporte.esporte.Esporte().alterarStatusCampeonato(campeonato_id=campeonato_id)
        return JsonResponse({'status': status, 'mensagem': mensagem})

    def put(self, *args, **kwargs):
        campeonato_id = self.request.data.get('id')
        nome = self.request.data.get('nome')
        season = self.request.data.get('season')
        imagem = self.request.data.get('imagem')
        status, mensagem = BO.esporte.esporte.Esporte().editar_campeonato(campeonato_id=campeonato_id, nome=nome,
                                                                          season=season, imagem=imagem)
        return JsonResponse({'status': status, 'mensagem': mensagem})

    def delete(self, *args, **kwargs):
        campeonato_id = self.request.data.get('id')
        status, mensagem = BO.esporte.esporte.Esporte().deletar_campeonato(campeonato_id=campeonato_id)
        return JsonResponse({'status': status, 'mensagem': mensagem})




class ApiCampeonato(APIView):
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        elif self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, *args, **kwargs):
        status, mensagem = BO.esporte.esporte.Esporte().get_campeonatos_api()
        return JsonResponse({'status': status, 'mensagem': mensagem})


class Aposta(APIView):

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
        evento_id = self.request.POST.get('eventoId')
        dados = BO.cliente.cliente.Cliente().simular_aposta(cpf_user=cpf_user,
                                                            evento_id=evento_id,
                                                                    campeonato=campeonato,
                                                                    time_1=time_1,
                                                                    time_2=time_2,
                                                                    odd=odd,
                                                                    tipo_aposta=tipo_aposta,
                                                                    valor=valor,
                                                                    is_aposta=is_aposta,
                                                                    casa_aposta=casa_aposta)
        return JsonResponse(dados)

    def delete(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')
        status, mensagem = BO.cliente.cliente.Cliente().deletar_cliente(cpf=cpf)
        return JsonResponse({'status': status, 'mensagem': mensagem})


class PegarOdds(APIView):

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get(self, *args, **kwargs):
        evento = self.request.GET.get('evento')
        tipo_aposta = self.request.GET.get('tipo_aposta')
        dados = BO.esporte.esporte.Esporte().get_odds(evento=evento, tipo_aposta=tipo_aposta)
        return JsonResponse({'list_odds': dados})

class PegarPredicoes(APIView):

    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get(self, *args, **kwargs):
        evento = self.request.GET.get('evento')
        dados = BO.esporte.esporte.Esporte().get_predicoes(evento_id=evento)
        return JsonResponse({'predicao': dados})


class PegarLive(APIView):
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get(self, *args, **kwargs):
        evento = self.request.GET.get('evento')
        dados = BO.esporte.esporte.Esporte().get_live( evento=evento)
        return JsonResponse({'campeonato': dados})

class EventoSimulado(APIView):

    def get(self, *args, **kwargs):
        cpf_user = self.request.GET.get('cpf_user')
        evento = self.request.GET.get('evento')
        dados = BO.cliente.cliente.Cliente().evento_simulado(cpf_user=cpf_user, evento=evento)
        return JsonResponse({'campeonato': dados})

class Dashboard(APIView):

    def get(self, *args, **kwargs):
        if validar_perfil(user=self.request.user, nivel_necessario=2):
            cpf_user = self.request.GET.get('cpf_user')
            dados, lista_tipos, lista_campeonatos = BO.cliente.cliente.Cliente().get_dashboard_cliente(cliente_id=cpf_user)
            return JsonResponse({'dados': dados, 'tipos':lista_tipos, 'campeonatos': lista_campeonatos})

class EventosFuturos(APIView):

    def get(self, *args, **kwargs):
        if validar_perfil(user=self.request.user, nivel_necessario=2):
            status, dados = BO.esporte.esporte.Esporte().get_eventos()

            return JsonResponse({'status':True,'dados': dados})

class EventosRecomendados(APIView):

    def get(self, *args, **kwargs):
        if validar_perfil(user=self.request.user, nivel_necessario=2):
            status, dados = BO.esporte.esporte.Esporte().get_recomendados(cliente=self.request.user)
            return JsonResponse({'status':True,'dados': dados})

class EventosCampeonatos(APIView):

    def get(self, *args, **kwargs):
        if validar_perfil(user=self.request.user, nivel_necessario=2):
            status, dados = BO.esporte.esporte.Esporte().get_eventos_campeonato(user=self.request.user)

            return JsonResponse({'status':status,'dados': dados})





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

class EfetuarPagamento(APIView):
    def post(self, *args, **kwargs):
        return JsonResponse({})

class ClienteCartao(APIView):

    def get(self, *args, **kwargs):
        cliente = self.request.GET.get('cliente_id')
        status, dados = BO.cliente.cliente.Cliente().pegar_cartao(cliente_id=cliente)
        return JsonResponse({'status': status, 'times': dados})

    def post(self, *args, **kwargs):
        cliente = self.request.GET.get('cliente')
        token_cartao= self.request.GET.get('token_cartao')
        ultimos_quatro_digitos= self.request.GET.get('ultimos_quatro_digitos')
        data_expiracao= self.request.GET.get('data_expiracao')
        nome_titular= self.request.GET.get('nome_titular')
        status, dados = BO.cliente.cliente.Cliente().criar_cartao(cliente=cliente,
                                                                  token_cartao=token_cartao,
                                                                  ultimos_quatro_digitos=ultimos_quatro_digitos,
                                                                  data_expiracao=data_expiracao,
                                                                  nome_titular=nome_titular,)
        return JsonResponse({'status': status, 'times': dados})

    def put(self, *args, **kwargs):
        cartao_id = self.request.GET.get('cartao_id')
        status, dados = BO.cliente.cliente.Cliente().editar_cartao(cartao_id=cartao_id)
        return JsonResponse({'status': status, 'times': dados})

    def delete(self, *args, **kwargs):
        cartao_id = self.request.GET.get('cartao_id')
        status, dados = BO.cliente.cliente.Cliente().deletar_cartao(cartao_id=cartao_id)
        return JsonResponse({'status': status, 'times': dados})

class SelecionarPlano(APIView):
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def post(self, *args, **kwargs):
        cpf = self.request.data.get('cpf')
        perfil_id = self.request.data.get('perfil_id')

        status, mensagem = BO.cliente.cliente.Cliente().selecionar_plano(cpf=cpf,perfil_id=perfil_id)
        return JsonResponse({'status': status, 'mensagem': mensagem})

class VerficarCodigo(APIView):
    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
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
        campeonatos = self.request.data.get('opcoes_campeonatos')
        cpf = self.request.data.get('cpf')
        valor = self.request.data.get('stack_aposta')


        status= BO.cliente.cliente.Cliente().cadastrar_preferencias(cpf=cpf,
                                                                    esportes=esporte,
                                                                    opcoes_apostas=opcoes_apostas,
                                                                    valor=valor,
                                                                    campeonatos=campeonatos
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

class AtualizarEventosOcorridos(APIView):
    def get(self, *args, **kwargs):
        data = self.request.GET.get('data')
        dados = BO.integracao.apifootball.Apifootball().atualizar_eventos_ocorridos(data=data)

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
            data_nasc = self.request.data.get('data_nasc')
            perfil = self.request.data.get('perfil_id')

            status, mensagem = BO.cliente.cliente.Cliente(username=username, password=password).editar_cliente(nome=nome,
                                                                                                               sobrenome=sobrenome,
                                                                                                               email=email,
                                                                                                               cpf=cpf,
                                                                                                               data_nasc=data_nasc,
                                                                                                               perfil=perfil)
        else:
            status, mensagem = False, 'essa conta não tem nivel de acesso o suficiente para editar'
        return JsonResponse({'status': status, 'mensagem': mensagem})