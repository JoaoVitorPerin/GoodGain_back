
import core.cliente.models
import core.esporte.models
import jwt
import datetime
import random
import ast
import json

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adicione campos personalizados ao token
        token['username'] = user.username
        token['cli_info'] = {
             'usuario_id': 123,
             'exp': (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).isoformat(),  # Expira em 30 minutos
             'iat': (datetime.datetime.utcnow()).isoformat(),
             'cli_info': {'cpf':user.cpf,
                          'nome':user.nome,
                          'sobrenome':user.sobrenome,
                          'email':user.email,
                          'perfil':{'perfil_id':user.perfil.pk,
                                    'perfil_nm_descritivo':user.perfil.nm_descritivo,
                                    'perfil_nivel':user.perfil.nivel}
                          },
         }

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.status:
            raise AuthenticationFailed('Conta inativa ou bloqueada')
        # Você pode adicionar informações adicionais ao response aqui, se necessário
        data['username'] = self.user.username

        return data

@staticmethod
def validar_perfil(user=None, nivel_necessario=3):
        if not user:
            raise PermissionDenied('usuário não foi fornecido')
        if user.perfil.nivel > nivel_necessario:
            raise PermissionDenied('usuário não possui nivel de acesso correto para acessar esta funcionalidade por favor faça um upgrade de conta')
        else:
            return True