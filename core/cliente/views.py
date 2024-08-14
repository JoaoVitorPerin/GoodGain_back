from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
import BO.cliente.cliente as bo_cliente
from rest_framework.views import APIView


# Create your views here.
class BuscaClienteCpf(View):
    # @method_decorator(login_required)
    def get(self, *args, **kwargs):
        cliente_id = self.request.GET.get('cliente_id')

        response = bo_cliente.Cliente()

        return JsonResponse(response, safe=False)

    @method_decorator(csrf_exempt)
    def post(self, *args, **kwargs):
        chave_cliente = self.request.POST.get('cliente_id', '').replace('.', '').replace('-', '')

        clientes = bo_cliente.Cliente.get_clientes_cpf(chave_cliente=chave_cliente)

        status = True if clientes else False
        descricao = '' if clientes else 'Nenhum cliente encontrado com as informações fornecidas'

        context = {
            'status': status,
            'descricao': descricao,
            'lista_clientes': [model_to_dict(cliente, exclude=['imagem', 'clube']) for cliente in clientes]
        }

        return JsonResponse(context, safe=False)


class BuscaClienteOutros(View):
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, *args, **kwargs):
        chave_cliente = self.request.POST.get('cliente_id')

        clientes = bo_cliente.Cliente.get_clientes_outros(chave_cliente=chave_cliente)

        status = True if clientes else False
        descricao = '' if clientes else 'Nenhum cliente encontrado com as informações fornecidas'

        context = {
            'status': status,
            'descricao': descricao,
            'lista_clientes': [model_to_dict(cliente, exclude=['imagem', 'clube']) for cliente in clientes]
        }

        return JsonResponse(context, safe=False)


# class Cadastrar(View):
#     """
#     :Nome da classe/função: CadastroView
#     :descrição: View de cadastro do usuário
#     :Criação: Nícolas Marinoni Grande - 18/08/2020
#     :Edições:
#     """
#
#     def get(self, *args, **kwargs):
#         """
#         :Nome da classe/função: get
#         :descrição: Função chamada quando é feita uma requisição GET para a View de cadastro do cliente
#         :Criação: Nícolas Marinoni Grande - 17/08/2020
#         :Edições:
#         :param args:
#         :param kwargs:
#         :return: View de Login com uma requisição GET
#         """
#         pass
#
#     def post(self, *args, **kwargs):
#         """
#         :Nome da classe/função: post
#         :descrição: Função chamada quando é feita uma requisição POST para a View de cadastro do cliente
#         :Criação: Nícolas Marinoni Grande - 17/08/2020
#         :Edições:
#         :param args:
#         :param kwargs:
#         :return: Status de cadastro
#         """
#
#         # cria o cliente
#         novo_cliente = bo_cliente.Cliente(
#             cpf_form=self.request.POST.get('cpf_cadastro'),
#             email=self.request.POST.get('email_cadastro'),
#             nm_completo=self.request.POST.get('nome_cadastro'),
#             dat_nasc=self.request.POST.get('nasc_cadastro'),
#             celular_completo_form=self.request.POST.get('tel_cadastro'),
#             telefone_completo_form=self.request.POST.get('telefone_opcional'),
#             sexo_codigo=self.request.POST.get('sexo_cadastro'),
#             termos=[termo.replace('termo-', '') for termo in self.request.POST if 'termo-' in termo],
#             request=self.request
#         )
#
#         status_criacao = novo_cliente.cadastrar(cep=self.request.POST.get('cep_cadastro'))
#         if status_criacao['status']:
#             cliente = status_criacao['cliente']
#             username = status_criacao['username']
#
#             BO.autenticacao.login.LoginCliente().criar(username=username, cliente_id=cliente.cpf, password=cliente.hash, request=self.request)
#
#         context = {
#             'status': status_criacao['status'],
#             'descricao': '',
#             'cliente': status_criacao['cliente']
#         }
#
#         return JsonResponse(context, safe=False)


class CadastrarEndereco(View):
    """
    :Nome da classe/função: CadastrarEnderecoView
    :descrição: View de cadastro de endereço de usuário por ajax
    :Criação: Nícolas Marinoni Grande - 18/08/2020
    :Edições:
    """

    def post(self, *args, **kwargs):
        """
        :Nome da classe/função: post
        :descrição: Função chamada quando é feita uma requisição post para a View cadastro de endereço
        :Criação: Nícolas Marinoni Grande - 17/08/2020
        :Edições:
        :param args:
        :param kwargs:
        :return: status de cadastro e (descrição do erro ou endereço cadastrado)
        """
        cliente_id = self.request.POST.get('cliente_id')
        cep = self.request.POST.get('cep')
        endereco = self.request.POST.get('rua')
        numero = self.request.POST.get('numero')
        complemento = self.request.POST.get('complemento')
        bairro = self.request.POST.get('bairro')
        nome = self.request.POST.get('nome')
        endereco_id = self.request.POST.get('endereco_id') if self.request.POST.get('endereco_id') != '' else None
        is_principal = True if self.request.POST.get('is_principal') == 'on' else False

        cliente = bo_cliente.Cliente(cliente_id=cliente_id).carregar_tudo()

        status_cadastro, endereco_id_novo = cliente.cadastrar_endereco(
            cep=cep,
            endereco=endereco,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            apelido=nome,
            is_principal=is_principal,
            endereco_id=endereco_id
        )
        if not status_cadastro:
            return JsonResponse({'status': False, 'descricao': 'Erro ao cadastrar endereço!'}, safe=False)
        else:
            return JsonResponse({'status': True, 'endereco_id': endereco_id_novo}, safe=False)

class Perfis(APIView):
    def get_permissions(self):
        """
        Instancia e retorna a lista de permissões que essa view requer.
        """
        if self.request.method == 'PUT':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get(self, *args, **kwargs):

        dados = bo_cliente.Cliente().get_perfis()

        return JsonResponse({'dados': dados})

    def put(self, *args, **kwargs):

        cpf = self.request.data.get('cpf')
        perfil_id = self.request.data.get('perfil_id')

        atualiza_perfis = bo_cliente.Cliente().editar_perfil_usuario(cpf=cpf, perfil_id=perfil_id)

        return JsonResponse({'Perfis': atualiza_perfis})

