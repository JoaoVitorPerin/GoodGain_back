"""
URL configuration for GoodGain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

import GoodGain.views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login', GoodGain.views.Login.as_view(), name='login'),
    re_path('cliente', GoodGain.views.Cliente.as_view(), name='cliente'),
    re_path('preferencias', GoodGain.views.Preferencias.as_view(), name='preferencias'),
    re_path('alterar/senha', GoodGain.views.AlterarsenhaView.as_view(), name='alterar_senha'),
    re_path('reset/senha', GoodGain.views.ResetSenhaView.as_view(), name='reset_senha'),
    re_path('verificar/codigo', GoodGain.views.VerficarCodigo.as_view(), name='reset_senha'),

    re_path('campeonato', GoodGain.views.Campeonato.as_view(), name='campeonato'),

    re_path('times/championship', GoodGain.views.GetCampeonatosTImes.as_view(), name='time_championship'),
    re_path('simular/aposta', GoodGain.views.SimularAposta.as_view(), name='simular_aposta'),


    #inicio variaveis do admin
    re_path('pegar_versus', GoodGain.views.PegarVersusu.as_view(), name='pegar_versus'),
    re_path('atualizar_dados', GoodGain.views.AtualizarDados.as_view(), name='atualizar_dados')
]
