from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

import core.cliente.views

urlpatterns = [
    # re_path('ajax/busca/cpf$', csrf_exempt(core.cliente.views.BuscaClienteCpf.as_view()), name='busca_cliente_cpf'),
    # re_path('ajax/busca/outros$', csrf_exempt(core.cliente.views.BuscaClienteOutros.as_view()), name='busca_cliente_outros'),
    # re_path('ajax/cadastrar$', csrf_exempt(core.cliente.views.Cadastrar.as_view()), name='cadastrar_cliente'),
    re_path(r'^ajax/cadastrar/endereco$', csrf_exempt(core.cliente.views.CadastrarEndereco.as_view()), name='cadastrar_endereco'),
    re_path(r'^ajax/buscar', core.cliente.views.BuscaClienteCpf.as_view(), name='buscar_cliente')
]
