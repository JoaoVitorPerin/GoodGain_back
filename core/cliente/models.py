import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from core.esporte.models import Campeonato

from core import esporte


class Cliente(AbstractBaseUser):
    """
    :Nome da classe/função: Cliente
    :descrição: Classe de clientes
    :Criação: Thiago Jungles Caron - 05/04/2024
    :Edições:
    """
    username = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    cpf = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    sobrenome = models.CharField(max_length=100, null=True)
    data_nascimento = models.IntegerField(null=True)
    imagem = models.CharField(max_length=200, null=True)
    is_email_confirmado = models.BooleanField(null=True, default=False)
    perfil = models.ForeignKey('cliente.Perfis', on_delete=models.DO_NOTHING, null=True)
    codigo_recuperacao = models.BigIntegerField(null=True)
    status = models.BooleanField(null=True, default=True)


    class Meta:
        db_table = u'"public\".\"cliente"'

class Perfis(models.Model):
    """
    :Nome da classe/função: Perfis
    :descrição: Classe de Perfis
    :Criação: Thiago Jungles Caron - 06/04/2024
    :Edições:
    """
    nome = models.CharField(max_length=100, primary_key=True)
    nm_descritivo = models.CharField(max_length=50, null=True)
    status = models.BooleanField(null=True, default=True)


    class Meta:
        db_table = u'"public\".\"perfis"'


class ClientePreferencias(models.Model):
    """
    :Nome da classe/função: ClientePreferencias
    :descrição: Classe de preferencias do cliente
    :Criação: Thiago Jungles Caron - 16/04/2024
    :Edições:
    """
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)
    esporte = models.CharField(max_length=500, null=True)
    campeonato = models.CharField(max_length=500, null=True)
    status = models.BooleanField(null=True, default=True)
    opcoes_apostas = models.CharField(max_length=500, null=True)


    class Meta:
        db_table = u'"public\".\"cliente_preferencias"'

class Aposta(models.Model):
    """
       :Nome da classe/função: Aposta
       :descrição: Classe de apostas dos clientes
       :Criação: João Vitor Perin - 29/05/2024
       :Edições:
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, null=True)
    campeonato = models.ForeignKey(Campeonato, on_delete=models.DO_NOTHING, null=True)
    status = models.BooleanField(null=True, default=True)
    timeA = models.CharField(max_length=100, null=True)
    timeB = models.CharField(max_length=100, null=True)
    valor = models.FloatField(null=True)
    odd = models.FloatField(null=True)

    class Meta:
        db_table = 'aposta'
