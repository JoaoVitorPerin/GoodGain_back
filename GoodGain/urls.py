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
    re_path('cadastro', GoodGain.views.CadastroCliente.as_view(), name='cadastro'),


    #inicio variaveis do admin
    re_path('pegar_versus', GoodGain.views.PegarVersusu.as_view(), name='pegar_versus')
]
