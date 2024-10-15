from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

import GoodGain.views
import core.cliente.views

urlpatterns = [
        re_path('cliente', GoodGain.views.Cliente.as_view(), name='cliente'),
        re_path('alterar/senha', GoodGain.views.AlterarsenhaView.as_view(), name='alterar_senha'),
        re_path('reset/senha', GoodGain.views.ResetSenhaView.as_view(), name='reset_senha'),
        re_path('verificar/codigo', GoodGain.views.VerficarCodigo.as_view(), name='reset_senha'),
]
