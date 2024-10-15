"""
URL configuration for GoodGain project.

The urlpatterns list routes URLs to views. For more information please see:
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
import GoodGain.views
import core.cliente.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path('login', GoodGain.views.Login.as_view(), name='login'),
    # re_path('validar_perfil', GoodGain.views.ValidarPerfil.as_view(), name='validar_perfil'),
    re_path(r'^login$', GoodGain.views.MyTokenObtainPairView.as_view()),
    re_path('cliente', GoodGain.views.Cliente.as_view(), name='cliente'),
    re_path('preferencias', GoodGain.views.Preferencias.as_view(), name='preferencias'),
    re_path('alterar/senha', GoodGain.views.AlterarsenhaView.as_view(), name='alterar_senha'),
    re_path('reset/senha', GoodGain.views.ResetSenhaView.as_view(), name='reset_senha'),
    re_path('verificar/codigo', GoodGain.views.VerficarCodigo.as_view(), name='reset_senha'),
    re_path('cliente/cartao', GoodGain.views.ClienteCartao.as_view(), name='cliente/cartao'),
    re_path('efetuar_pagamento', GoodGain.views.VerficarCodigo.as_view(), name='efetuar_pagamento'),

    path('campeonato', GoodGain.views.Campeonato.as_view(), name='campeonato'),

    path('api_campeonato', GoodGain.views.ApiCampeonato.as_view(), name='api_campeonato'),

    re_path('times/championship', GoodGain.views.GetCampeonatosTImes.as_view(), name='time_championship'),
    re_path('simular/aposta', GoodGain.views.Aposta.as_view(), name='simular_aposta'),
    re_path('evento/simulado', GoodGain.views.EventoSimulado.as_view(), name='evento_simulado'),
    re_path('pegar/odds', GoodGain.views.PegarOdds.as_view(), name='pegar_odds'),
    re_path('pegar/predicoes', GoodGain.views.PegarPredicoes.as_view(), name='pegar_predicoes'),
    re_path('live/evento', GoodGain.views.PegarLive.as_view(), name='live_evento'),

    re_path('futuros/eventos', GoodGain.views.EventosFuturos.as_view(), name='futuros_eventos'),
    re_path('home_info_usuarios', GoodGain.views.EventosCampeonatos.as_view(), name='home_preferencias'),
    # re_path('futuros/eventos', GoodGain.views.EventosRecomendados.as_view(), name='eventos_recomendados'),
    re_path('dashboard', GoodGain.views.Dashboard.as_view(), name='dashboard'),
    re_path('historico', GoodGain.views.Historico.as_view(), name='historico'),


    #inicio variaveis do admin
    re_path('atualizar_dados', GoodGain.views.AtualizarDados.as_view(), name='atualizar_dados'),
    re_path('atualizar_eventos_ocorridos', GoodGain.views.AtualizarEventosOcorridos.as_view(), name='atualizar_eventos_ocorridos'),
    re_path('listar_usuarios', GoodGain.views.ListarUsarios.as_view(), name='listar_usuarios'),
    re_path('listar_log', GoodGain.views.ListarLogs.as_view(), name='listar_log'),
    re_path('listar_operacoes', GoodGain.views.ListaOperacoes.as_view(), name='listar_operacoes'),
    re_path('editar_usuario', GoodGain.views.EditarUsuarioAdmin.as_view(), name='editar_usuario'),
    re_path('listar_perfis', core.cliente.views.Perfis.as_view(), name='listar_perfis'),


]