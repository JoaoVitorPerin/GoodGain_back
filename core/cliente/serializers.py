from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
import core.cliente.models
import core.serializers
import BO.cliente.cliente
import ecommerce.clube.models
import util.DateTime


class EnderecoSerializer(core.serializers.DynamicFieldsModelSerializer):
    cep = core.serializers.CepSerializer()
    municipio = serializers.SerializerMethodField()
    cep_form = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    uf = serializers.SerializerMethodField()

    class Meta:
        model = core.cliente.models.Endereco
        fields = '__all__'

    @staticmethod
    def get_municipio(instance):
        municipio = instance.cep.municipio.nome
        return municipio

    @staticmethod
    def get_cep_form(instance):
        cep_form = instance.cep.cep_form
        return cep_form

    @staticmethod
    def get_estado(instance):
        estado = instance.cep.municipio.uf.nome
        return estado

    @staticmethod
    def get_uf(instance):
        uf = instance.cep.municipio.uf.nm_abrev
        return uf


class ClubeSerializer(core.serializers.DynamicFieldsModelSerializer):
    nome = serializers.CharField()

    class Meta:
        model = ecommerce.clube.models.Clube
        fields = '__all__'


class TermoSerializer(core.serializers.DynamicFieldsModelSerializer):
    tipo = serializers.IntegerField(source='tipo_codigo')

    class Meta:
        model = core.cliente.models.Termo
        fields = '__all__'


class ClienteTermoSerializer(core.serializers.DynamicFieldsModelSerializer):
    class Meta:
        model = core.cliente.models.ClienteTermo
        fields = '__all__'


class ClienteSerializer(core.serializers.DynamicFieldsModelSerializer):
    id = serializers.IntegerField(source='cpf')
    celular = serializers.CharField(source='celular_completo_form')
    rg = serializers.CharField()
    rg_form = serializers.CharField()
    telefone = serializers.CharField(source='telefone_completo_form')
    dat_nascimento = serializers.DateField(source='dat_nasc')
    origem_filial = serializers.IntegerField(source='origem_filial_id')
    origem_funcionario = serializers.CharField(source='origem_funcionario_id')
    origem_codigo = serializers.CharField()
    sexo_codigo = serializers.CharField()
    dat_cadastro = serializers.DateTimeField(source='dat_insercao')
    passaporte = serializers.CharField(source='passaporte_form')

    cr_numero = serializers.CharField(source='cr_codigo')
    cr_uf = serializers.IntegerField(source='cr_uf_id')
    cr_codigo = serializers.CharField(source='cr_tipo_codigo')

    clube = serializers.SerializerMethodField()
    sexo = serializers.SerializerMethodField()
    termos = serializers.SerializerMethodField()
    termos_cliente = serializers.SerializerMethodField()
    # dat_nascimento = serializers.SerializerMethodField()

    assinatura = serializers.SerializerMethodField('get_assinatura')

    optin_sms = serializers.SerializerMethodField()
    optin_email = serializers.SerializerMethodField()
    optin = serializers.SerializerMethodField()

    endereco_principal = serializers.SerializerMethodField()
    enderecos = serializers.SerializerMethodField()
    cd_endereco = serializers.SerializerMethodField()

    dat_anonimizacao_ecom = serializers.SerializerMethodField()
    dat_cadastro_ecom = serializers.SerializerMethodField()

    cd_dependencia = serializers.SerializerMethodField()

    class Meta:
        model = core.cliente.models.Cliente
        fields = '__all__'

    @staticmethod
    def get_dat_anonimizacao_ecom(instance):
        try:
            return util.DateTime.datetime_to_str(instance.dat_anonimizacao, '%d/%m/%Y')
        except:
            return ''

    @staticmethod
    def get_dat_cadastro_ecom(instance):

        try:
            return util.DateTime.datetime_to_str(instance.clientelogin.dat_insercao, '%d/%m/%Y')
        except:
            return ''

    @staticmethod
    def get_endereco_principal(instance):
        endereco_principal = instance.endereco_set.all().filter(status=True).order_by('-is_principal', 'id').first()
        return EnderecoSerializer(endereco_principal, fields=['id', 'cep_form', 'endereco', 'numero',
                                                              'complemento', 'bairro', 'municipio', 'estado', 'uf']).data

    @staticmethod
    def get_clube(instance):
        clube = instance.clube_clientes.all().filter(tipo_codigo='clube').order_by('-prioridade').first()
        return ClubeSerializer(clube, fields=['nome']).data

    @staticmethod
    def get_optin_sms(instance):
        termo = 'ofertas_sms'
        is_termo = instance.clientetermo_set.all().filter(termo__status=True, status=True).filter(Q(termo__nome=termo) | Q(termo__termo_pai__nome=termo)).exists()
        return is_termo

    @staticmethod
    def get_optin_email(instance):
        termo = 'ofertas_email'
        is_termo = instance.clientetermo_set.all().filter(termo__status=True, status=True).filter(Q(termo__nome=termo) | Q(termo__termo_pai__nome=termo)).exists()
        return is_termo

    @staticmethod
    def get_optin(instance):
        termo = 'termos_uso'
        #is_termo = instance.clientetermo_set.all().filter(termo__status=True, status=True).filter(Q(termo__nome=termo) | Q(termo__termo_pai__nome=termo)).exists()
        try:
            is_termo = instance.clientelogin is not None
        except:
            is_termo = False

        return is_termo

    @staticmethod
    def get_enderecos(instance):
        enderecos = instance.endereco_set.all().order_by('-is_principal', 'id')
        return EnderecoSerializer(enderecos, many=True, fields=['id', 'cep_form', 'endereco', 'numero',
                                                                'complemento', 'municipio', 'estado', 'uf']).data

    @staticmethod
    def get_sexo(instance):
        sexo = instance.sexo.nome if instance.sexo else None
        return sexo

    # @staticmethod
    # def get_dat_nascimento(instance):
    #     dat_nasc = str(instance.dat_nasc).replace('-' , '')
    #     return dat_nasc

    @staticmethod
    def get_termos_cliente(instance):
        termos = BO.cliente.cliente.Cliente(cliente=instance).pegar_termos()
        return termos

    @staticmethod
    def get_termos(instance):
        termos = BO.cliente.cliente.Cliente.get_todos_termos_ecom()
        return termos

    @staticmethod
    def get_assinatura(instance):
        try:
            assinatura = instance.assinatura.name
        except:
            assinatura = None
        return assinatura

    @staticmethod
    def get_cd_dependencia(instance):
        try:
            dependencia = instance.id
        except:
            dependencia = None
        return dependencia

    @staticmethod
    def get_cd_endereco(instance):
        try:
            endereco_id = instance.endereco_id
        except:
            endereco_id = None
        return endereco_id

class DependenteSerializer(core.serializers.DynamicFieldsModelSerializer):

    class Meta:
        model = core.cliente.models.Dependente
        fields = '__all__'


class OportunidadeContatoSerializer(core.serializers.DynamicFieldsModelSerializer):
    cliente_cpf = serializers.SerializerMethodField()
    cliente_nome = serializers.SerializerMethodField()
    cliente_telefone = serializers.SerializerMethodField()
    produto_nome = serializers.SerializerMethodField()
    funcionario_contato_nome = serializers.SerializerMethodField()
    descricao_status = serializers.SerializerMethodField()

    class Meta:
        model = core.cliente.models.OportunidadeContato
        fields = '__all__'

    @staticmethod
    def get_cliente_telefone(instance):
        try:
            return instance.cliente.celular_completo_form or instance.cliente.telefone_completo_form
        except:
            return None

    @staticmethod
    def get_funcionario_contato_nome(instance):
        try:
            return instance.funcionario_contato.nm_completo
        except:
            return None

    @staticmethod
    def get_cliente_nome(instance):
        try:
            return instance.cliente.nm_completo
        except:
            return None

    @staticmethod
    def get_cliente_cpf(instance):
        try:
            return instance.cliente.cpf_form
        except:
            return None

    @staticmethod
    def get_produto_nome(instance):
        try:
            return instance.produto.nome
        except:
            return None

    @staticmethod
    def get_descricao_status(instance):
        try:
            return '{} - {}'.format(str(instance.log_status.ordem).zfill(2), instance.log_status.nm_descritivo)
        except:
            return None
