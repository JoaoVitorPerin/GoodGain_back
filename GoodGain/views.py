from django.http import JsonResponse

import BO.cliente.cliente
from rest_framework.views import APIView

class CadastroCliente(APIView):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        nome = self.request.POST.get('nome')
        sobrenome = self.request.POST.get('sobrenome')
        email = self.request.POST.get('email')
        cpf = self.request.POST.get('cpf')
        data_nasc = self.request.POST.get('data_nasc')

        status = BO.cliente.cliente.Cliente(username=username, password=password).cadastrar_cliente(nome=nome,
                                                                                                    sobrenome=sobrenome,
                                                                                                    email=email,
                                                                                                    cpf=cpf,
                                                                                                    data_nasc=data_nasc)

        return status
class Login(APIView):
    def get(self, *args, **kwargs):
        return

    def post(self, *args, **kwargs):
        user = self.request.POST.get('username')
        password = self.request.POST.get('password')

        status, descricao, token_jwt = BO.cliente.cliente.Cliente(username=user, password=password).logar()

        return JsonResponse({'status': status,'descricao': descricao,'token_jwt': token_jwt})