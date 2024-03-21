from django.http import JsonResponse

import BO.cliente.cliente


class CadastroCliente():
    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        nome_completo = self.request.POST.get('password')
        cpf = self.request.POST.get('cpf')
        data_nasc = self.request.POST.get('data_nasc')

        status, descricao = BO.cliente.cliente.Cliente(email=email, password=password).cadastrar_cliente(nome_completo=nome_completo,
                                                                                                cpf=cpf,
                                                                                                data_nasc=data_nasc)

        context = {
            'status': status,
            'descricao':descricao
        }

        return JsonResponse(context)
class Login():
    def get(self, *args, **kwargs):
        return
    def post(self, *args, **kwargs):
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')

        status = BO.cliente.cliente.Cliente(email=email, password=password).logar()
        context = {
            'status': status,
        }

        return JsonResponse(context)