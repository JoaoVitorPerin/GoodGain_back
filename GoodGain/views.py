from django.http import JsonResponse

import BO.cliente.cliente
from rest_framework.views import APIView

class CadastroCliente(APIView):
    def post(self, *args, **kwargs):
        user = self.request.POST.get('user')
        password = self.request.POST.get('password')
        nome_completo = self.request.POST.get('password')
        cpf = self.request.POST.get('cpf')
        data_nasc = self.request.POST.get('data_nasc')

        status = BO.cliente.cliente.Cliente(username=user, password=password).logar()

        return status
class Login(APIView):
    def get(self, *args, **kwargs):
        return

    def post(self, *args, **kwargs):
        user = self.request.POST.get('username')
        password = self.request.POST.get('password')

        status = BO.cliente.cliente.Cliente(username=user, password=password).logar()

        return JsonResponse({'status': status})