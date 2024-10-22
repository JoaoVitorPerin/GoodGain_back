import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

from core import esporte
import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models


class ClienteManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O campo User é obrigatório')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True')

        return self.create_user(username, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)

class Cliente(AbstractBaseUser):
    username = models.CharField(max_length=100, null=True, unique=True)
    email = models.CharField(max_length=100, null=True)
    cpf = models.BigIntegerField(primary_key=True)
    nome = models.CharField(max_length=100, null=True)
    sobrenome = models.CharField(max_length=100, null=True)
    data_nascimento = models.IntegerField(null=True)
    imagem = models.CharField(max_length=200, null=True)
    is_email_confirmado = models.BooleanField(default=False, null=True)
    perfil = models.ForeignKey('cliente.Perfis', on_delete=models.DO_NOTHING, null=True)
    codigo_recuperacao = models.BigIntegerField(null=True)
    status = models.BooleanField(default=True, null=True)
    stack_aposta = models.FloatField(null=True, default=00.00)

    objects = ClienteManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = '"public"."cliente"'


class ClienteCarteira(models.Model):
    """
    :Nome da classe/função: Perfis
    :descrição: Classe de Perfis
    :Criação: Thiago Jungles Caron - 06/04/2024
    :Edições:
    """
    nome = models.CharField(max_length=100)
    status = models.BooleanField(null=True, default=True)
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)
    token_cartao = models.CharField(max_length=1000, null=True)
    ultimos_quatro_digitos = models.CharField(max_length=1000, null=True)
    data_expiracao = models.CharField(max_length=1000, null=True)
    nome_titular = models.CharField(max_length=1000, null=True)


    class Meta:
        db_table = u'"public\".\"cliente_carteira"'


class ClienteAssinatura(models.Model):
    """
    :Nome da classe/função: Perfis
    :descrição: Classe de Perfis
    :Criação: Thiago Jungles Caron - 06/04/2024
    :Edições:
    """
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)
    perfil = models.ForeignKey('cliente.Perfis', on_delete=models.DO_NOTHING, null=True)
    data = models.CharField(max_length=40, null=True)
    status = models.BooleanField(null=True, default=True)
    acao = models.CharField(max_length=1000, null=True)


    class Meta:
        db_table = u'"public\".\"log_assinaturas"'




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
    valor = models.FloatField(null=True)
    nivel = models.IntegerField(null=True)


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
    id_preferencia = models.CharField(max_length=500, null=True)
    status = models.BooleanField(null=True, default=True)
    tipo_preferencia = models.CharField(max_length=500, null=True)



    class Meta:
        db_table = u'"public\".\"cliente_preferencias"'


class Aposta(models.Model):
    """
       :Nome da classe/função: Aposta
       :descrição: Classe de apostas dos clientes
       :Criação: Thiago Jungles Caron - 16/04/2024
       :Edições:
       """
    cliente = models.ForeignKey('cliente.Cliente', on_delete=models.DO_NOTHING, null=True)
    status = models.BooleanField(null=True, default=True)
    evento = models.ForeignKey('esporte.Evento', on_delete=models.DO_NOTHING, null=True)
    campeonato = models.ForeignKey('esporte.Campeonato',on_delete=models.DO_NOTHING, null=True)
    time_1 = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='time_1')
    time_2 = models.ForeignKey('esporte.Time', on_delete=models.DO_NOTHING, null=True, related_name='time_2')
    odd = models.CharField(max_length=500, null=True)
    valor = models.FloatField(null=True)
    tipo_aposta = models.CharField(max_length=500, null=True)
    casa_aposta = models.CharField(max_length=500, null=True)
    is_aposta = models.BooleanField(null=True, default=False)


    class Meta:
        db_table = u'"public\".\"aposta"'