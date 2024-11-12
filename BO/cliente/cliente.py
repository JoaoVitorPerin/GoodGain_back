from django.http import HttpResponseServerError

import core.cliente.models
import core.esporte.models
import jwt
import datetime
import pytz
import random
import ast
import json

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


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

class Cliente():
     def __init__(self, username=None, password=None):
         self.username = username
         self.password = password

     @staticmethod
     def limpar_cpf(cpf):
         if cpf is None:
             return ""
         return cpf.replace(".", "").replace("-", "")

     @staticmethod
     def limpar_data(data):
         if '/' in data:
             partes = data.split('/')

             # Verifica se a data já está no formato 'yyyy/mm/dd'
             if len(partes) == 3 and len(partes[0]) == 4 and len(partes[1]) == 2 and len(partes[2]) == 2:
                 # Retorna a data como está se já estiver no formato correto
                 pass
             # Caso contrário, assume que a data está em 'dd/mm/yyyy' e rearranja para 'yyyy/mm/dd'
             elif len(partes) == 3 and len(partes[0]) == 2 and len(partes[1]) == 2 and len(partes[2]) == 4:
                 data = f'{partes[2]}/{partes[1]}/{partes[0]}'

             # Retorna uma mensagem de erro se o formato não for reconhecido
             else:
                 return "Formato de data inválido"
             if data is None:
                 return ""
             return data.replace("/", "").replace("-", "")
         else:
             return data

     def pegar_cartao(self,cliente_id=None):
         return

     def editar_cartao(self):
         return

     def criar_cartao(self,cliente=None,token_cartao=None,ultimos_quatro_digitos=None,data_expiracao=None,nome_titular=None):
         return

     def deletar_cartao(self):
         return

     def get_cliente(self, cpf=None):
        try:
            cliente = core.cliente.models.Cliente.objects.values().filter(cpf=cpf).first()
            return True, '', cliente
        except:
            return False, '', {}

     def get_perfis(self):
        return list(core.cliente.models.Perfis.objects.values().filter(status=True))

     def editar_perfil_usuario(self, cpf=None, perfil_id=None):
         try:
             _, _, cliente_existe = self.get_cliente(cpf=Cliente.limpar_cpf(cpf))
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
             cliente = core.cliente.models.Cliente.objects.filter(cpf=Cliente.limpar_cpf(cpf)).first()
             if not cliente:
                 return False, 'esse cliente não existe'
             if perfil_id is None:
                 return False, 'esse perfil não existe'
             cliente.perfil_id = perfil_id
             cliente.save()
             return True

         except Exception as e:  # Captura a exceção e armazena na variável e # Imprime ou faça log da exceção para ver o erro exato
             return False  # Retorna a mensagem de erro


     def get_apostas_cliente(self,cpf_user=None):
        try:
            lista_apostas_cliente_tratada = []
            lista_apostas_cliente = list(core.cliente.models.Aposta.objects.values(
'cliente_id',
'status',
'evento',
'campeonato__nome',
'time_1__nome',
'time_2__nome',
'odd',
'valor',
'tipo_aposta',
'is_aposta','evento__resultado_partida').filter(cliente_id=cpf_user, is_aposta=True).order_by('-id'))
            # verificar resultado da aposta

            tipos_aposta= core.esporte.models.Tipo.objects.values().filter(tipo= 'OPCOES.APOSTA', status=True)
            dict_apostas = {}
            for tipo in tipos_aposta:
                dict_apostas[tipo.get('id')] = tipo.get('informacao')


            for aposta in lista_apostas_cliente:
                aposta['nome_tipo_aposta'] = dict_apostas[int(aposta['tipo_aposta'])]
                if aposta.get('evento__resultado_partida') is not None:
                    resultado_da_partida = json.loads(aposta.get('evento__resultado_partida'))
                    data_hora_especificada = datetime.datetime.fromisoformat(resultado_da_partida[0]['fixture']['date'])

                    # Obter a data e hora atual no mesmo fuso horário
                    data_hora_atual = datetime.datetime.now(pytz.utc)

                    # Comparar as datas

                    if data_hora_atual >= data_hora_especificada:
                        # verificação de tipo de aposta 2.5+
                        if aposta.get('tipo_aposta') == '5':
                           if resultado_da_partida[0]['goals']['home'] + resultado_da_partida[0]['goals']['away'] >= 2:
                               aposta['status_aposta'] = 'ACERTOU'
                               lista_apostas_cliente_tratada.append(aposta)
                               continue
                           else:
                               aposta['status_aposta'] ='NÃO ACERTOU'
                               lista_apostas_cliente_tratada.append(aposta)
                               continue

                        # verificação de tipo de aposta ambas marcam
                        if aposta.get('tipo_aposta') == '8':
                           if resultado_da_partida[0]['goals']['home'] >=1 and resultado_da_partida[0]['goals']['away'] >= 1:
                               aposta['status_aposta'] = 'ACERTOU'
                               lista_apostas_cliente_tratada.append(aposta)
                               continue
                           else:
                               aposta['status_aposta'] ='NÃO ACERTOU'
                               lista_apostas_cliente_tratada.append(aposta)
                               continue
                    else:
                        aposta['status_aposta'] = 'EM ANDAMENTO'
                else:
                    aposta['status_aposta'] = 'EM ANDAMENTO'
            return True, lista_apostas_cliente
        except:
            return False, []

     def get_dashboard_cliente(self, cliente_id=None):
         try:
             # Filtra as apostas do cliente com is_aposta=True
             apostas_cliente = list(core.cliente.models.Aposta.objects.filter(cliente_id=cliente_id, is_aposta=True))

             dict_campeonatos = {}
             dict_tipo_apostas = {}
             todas_odds = 0
             valor_apostado = 0.0
             valor_anterior = 0
             tipo_aposta_mais_escolhida = 'nenhuma'

             tipos_apostas = {
                 tipo['id']: tipo['informacao']
                 for tipo in core.esporte.models.Tipo.objects.values('id', 'informacao')
             }

             # Processa as apostas para calcular os dados do dashboard
             for aposta in apostas_cliente:
                 # Contagem de campeonatos
                 if aposta.campeonato_id not in dict_campeonatos:
                     dict_campeonatos[aposta.campeonato_id] = 1
                 else:
                     dict_campeonatos[aposta.campeonato_id] += 1

                 # Contagem de tipos de apostas
                 if aposta.tipo_aposta not in dict_tipo_apostas:
                     dict_tipo_apostas[aposta.tipo_aposta] = 1
                 else:
                     dict_tipo_apostas[aposta.tipo_aposta] += 1

                 # Soma das odds
                 todas_odds += float(aposta.odd) if aposta.odd else 0

                 # Soma do valor apostado
                 valor_apostado += aposta.valor if aposta.valor is not None else 0

             # Cálculo das médias
             media_odds = todas_odds / len(apostas_cliente) if len(apostas_cliente) > 0 else 0.0
             media_valor_apostado = valor_apostado / len(apostas_cliente) if len(apostas_cliente) > 0 else 0.0

             # Determinar o tipo de aposta mais escolhido
             for tipo_aposta, valor_atual in dict_tipo_apostas.items():
                 if valor_atual > valor_anterior:
                     valor_anterior = valor_atual
                     tipo_aposta_mais_escolhida = tipo_aposta

             # Lista para os gráficos
             lista_grafico_campeonato = [{'campeonato': campeonato, 'valor': valor}
                                         for campeonato, valor in dict_campeonatos.items()]
             lista_grafico_tipo = [{'tipo_aposta': tipo_aposta, 'valor': valor}
                                   for tipo_aposta, valor in dict_tipo_apostas.items()]

             # Serializa a tabela de apostas
             tabela_aposta = [
                 {
                     'id': aposta.id,
                     'campeonato_id': aposta.campeonato.nome if aposta.campeonato else None,
                     'tipo_aposta_nome': tipos_apostas.get(int(aposta.tipo_aposta), 'Desconhecido'),
                     'odd': aposta.odd,
                     'valor': aposta.valor,
                     'time_1': aposta.time_1.nome if aposta.time_1 else None,
                     'time_2': aposta.time_2.nome if aposta.time_2 else None
                 }
                 for aposta in apostas_cliente
             ]

             # Dados de retorno
             dados = {
                 'status': True,
                 'qtd_apostas': len(apostas_cliente),
                 'media_odds': media_odds,
                 'valor_apostado': media_valor_apostado,
                 'tipo_aposta_mais_escolhida': tipo_aposta_mais_escolhida,
                 'grafico_campeonatos': lista_grafico_campeonato,
                 'grafico_tipo_aposta': lista_grafico_tipo,
                 'tabela_aposta': tabela_aposta
             }

             # Lista de tipos e campeonatos
             lista_tipos = list(core.esporte.models.Tipo.objects.values('id', 'informacao'))
             lista_campeonatos = list(core.esporte.models.Campeonato.objects.values('id', 'nome'))

             return dados, lista_tipos, lista_campeonatos

         except Exception as e:
             # Retorna erro em caso de exceção
             return {'status': False, 'error': str(e)}, [], []

     def vitoria_time_a(self, time_a=None, campeonato=None, evento_id=None):
         try:
            campeonato_info = core.esporte.models.Campeonato.objects.filter(id=campeonato).values().first()
            if not campeonato_info:
                return {'status': False, 'resultado':0}
            performace_time = core.esporte.models.PerformaceTime.objects.values().filter(time_id=time_a, season=campeonato_info['season_atual']).first()

            vitorias = 0
            empates = 0
            informacoes_time = json.loads(performace_time.get('info'))

            vitorias = informacoes_time['fixtures']['wins']['total'] *3

            empates = informacoes_time['fixtures']['draws']['total']



            return {'status':True,'resultado':vitorias + empates + 2}
         except:
            return {'status':True, 'resultado': 0}

     def vitoria_time_b(self, time_b=None, campeonato=None, evento_id=None):
         try:
             campeonato_info = core.esporte.models.Campeonato.objects.filter(id=campeonato).values().first()
             if not campeonato_info:
                 return {'status': False, 'resultado': 0}
             performace_time = core.esporte.models.PerformaceTime.objects.values().filter(time_id=time_b,
                                                                                          season=campeonato_info[
                                                                                              'season_atual']).first()

             vitorias = 0
             empates = 0
             informacoes_time = json.loads(performace_time.get('info'))

             vitorias = informacoes_time['fixtures']['wins']['total'] * 3

             empates = informacoes_time['fixtures']['draws']['total']

             return {'status': True, 'resultado': vitorias + empates}
         except:
             return {'status': True, 'resultado': 0}

     def simular_aposta(self, casa_aposta=None, evento_id=None, cpf_user=None, campeonato=None, time_1=None, time_2=None, odd=None,tipo_aposta=None, valor=None, is_aposta=False):
         # TODO Lembre que todo e qualquer calculo que for criado nessa etapa devera ser adicionado ao fluxo de precalculo
         if tipo_aposta == '5':
             dados, html_retorno = self.calcular_2_5(odd=odd, campeonato=campeonato, time_1=time_1, time_2=time_2)
         elif tipo_aposta == '8':
             dados, html_retorno = self.calcular_ambos_marcam(odd=odd, campeonato=campeonato, time_1=time_1, time_2=time_2)

         if dados.get('status'):
             aposta = core.cliente.models.Aposta()
             aposta.evento_id = evento_id
             aposta.cliente_id = cpf_user
             aposta.status = True
             aposta.campeonato_id = campeonato
             aposta.time_1_id = time_1
             aposta.time_2_id = time_2
             aposta.odd = odd
             aposta.valor = valor
             aposta.tipo_aposta = tipo_aposta
             aposta.is_aposta = True if is_aposta == 'true' else False
             aposta.casa_aposta = casa_aposta
             aposta.save()


         return {'html_retorno':html_retorno}

     def evento_simulado(self, cpf_user=None, evento=None, odd=None):
         try:
             evento = core.esporte.models.Evento.objects.values().filter(id=evento).first()

             return evento
         except:
            return []

     def calcular_2_5(self, odd=None, campeonato=None, time_1=None, time_2=None):
         try:
             context = {
                 'media_mandante_casa': 0.0,
                 'media_visitante_fora': 0.0,
                 'media_total_mandante': 0.0,
                 'media_total_visitante': 0.0,
                 'previsao_gols': 0.0,
                 'class_descricao': '',
                 'descricao': 'Erro',
                 'status': True
             }

             # (média
             #  de gols marcados / sofridos casa time 1 + média de gols marcados / sofridos fora time 2 + média de gols marcados
             #  / sofridos geral time 1 + média de gols marcados + sofridos geral time 2) / 4
             season_campeonato = core.esporte.models.Campeonato.objects.values_list('season_atual', flat=True).filter(id=campeonato)
             performace_time_1 = json.loads(core.esporte.models.PerformaceTime.objects.values_list('info', flat=True).filter(time_id=time_1, season=season_campeonato[0]).first())
             performace_time_2 = json.loads(core.esporte.models.PerformaceTime.objects.values_list('info', flat=True).filter(time_id=time_2, season=season_campeonato[0]).first())
             #Média de gols marcados + sofridos na condição do mandante, média de gols marcados + sofridos na condição do visitante, e as duas médias gerais desses dois times no campeonato
             media_mandante_casa = float(performace_time_1['goals']['against']['average']['home']) + float(performace_time_1['goals']['for']['average']['home'])
             media_visitante_fora = float(performace_time_2['goals']['against']['average']['home']) + float(performace_time_2['goals']['for']['average']['home'])
             media_total_mandante = float(performace_time_1['goals']['against']['average']['total']) + float(performace_time_1['goals']['for']['average']['total'])
             media_total_visitante = float(performace_time_2['goals']['against']['average']['total']) + float(performace_time_2['goals']['for']['average']['total'])
             previsao_gols = (media_mandante_casa + media_visitante_fora + media_total_mandante + media_total_visitante)/4
             if previsao_gols >= 3:
                descricao = 'Aposta muito recomendada'
                class_descricao = 'muito-recomendado'
             elif previsao_gols >= 2.7:
                descricao = 'Aposta recomendada'
                class_descricao = 'recomendado'
             elif previsao_gols >= 2.5:
                descricao = 'Aposta arriscada'
                class_descricao = 'arriscado'
             elif previsao_gols < 2.5 and previsao_gols > 2.4:
                descricao = 'Aposta não recomendada'
                class_descricao = 'nao-recomendado'
             else:
                descricao = 'Não investir'
                class_descricao = 'nao-investir'

             context ={
            'media_mandante_casa':media_mandante_casa,
            'media_visitante_fora':media_visitante_fora,
            'media_total_mandante':media_total_mandante,
            'media_total_visitante':media_total_visitante,
            'previsao_gols':previsao_gols,
            'descricao': descricao,
            'status': True,
            'class_descricao': class_descricao
             }


             html_content = render_to_string('retorno2.5gols.html', context)



             return context , html_content
         except:
             context['status'] = False
             return context,  html_content

     def calcular_ambos_marcam(self, odd=None, campeonato=None, time_1=None, time_2=None):
         try:
             context = {
                 'media_mandante_casa': 0.0,
                 'media_visitante_fora': 0.0,
                 'media_total_mandante': 0.0,
                 'media_total_visitante': 0.0,
                 'previsao_gols': 0.0,
                 'descricao': 'Erro',
                 'status': True
             }

             # (média
             #  de gols marcados / sofridos casa time 1 + média de gols marcados / sofridos fora time 2 + média de gols marcados
             #  / sofridos geral time 1 + média de gols marcados + sofridos geral time 2) / 4
             season_campeonato = core.esporte.models.Campeonato.objects.values_list('season_atual', flat=True).filter(id=campeonato)
             performace_time_1 = json.loads(core.esporte.models.PerformaceTime.objects.values_list('info', flat=True).filter(time_id=time_1, season=season_campeonato[0]).first())
             performace_time_2 = json.loads(core.esporte.models.PerformaceTime.objects.values_list('info', flat=True).filter(time_id=time_2, season=season_campeonato[0]).first())
             #Média de gols marcados + sofridos na condição do mandante, média de gols marcados + sofridos na condição do visitante, e as duas médias gerais desses dois times no campeonato
             media_mandante_marcados = float(performace_time_1['goals']['for']['average']['total'])
             media_mandante_sofridos = float(performace_time_1['goals']['against']['average']['total'])
             media_visitante_marcados =float(performace_time_2['goals']['for']['average']['total'])
             media_visitante_sofridos =float(performace_time_2['goals']['against']['average']['total'])
             media_mandante = (media_mandante_marcados + media_visitante_sofridos)/2
             media_visitante= (media_visitante_marcados + media_mandante_sofridos)/2
             media_geral = (media_mandante + media_visitante)/2


             if media_mandante >=1.45:
                 descricao_mandante = 'Aposta recomendado'
             elif media_mandante >=1.1:
                 descricao_mandante = 'Aposta arriscada'
             else:
                 descricao_mandante = 'Não investir'

             if media_visitante >=1.45:
                 descricao_visitante = 'Aposta recomendado'
             elif media_visitante >=1.1:
                 descricao_visitante = 'Aposta arriscada'
             else:
                 descricao_visitante = 'Não investir'

             if media_geral >=1.45:
                 descricao_geral = 'Aposta recomendado'
             else:
                 descricao_geral = 'Não investir'

             context ={
            'media_mandante_marcados':media_mandante_marcados,
            'media_mandante_sofridos':media_mandante_sofridos,
            'media_visitante_marcados':media_visitante_marcados,
            'media_visitante_sofridos':media_visitante_sofridos,
            'media_mandante':media_mandante,
            'media_visitante':media_visitante,
            'media_geral':media_geral,
            'descricao_mandante': descricao_mandante,
            'descricao_visitante': descricao_visitante,
            'descricao_geral': descricao_geral,
            'status': True
             }


             html_content = render_to_string('ambosmarcam.html', context)



             return context , html_content
         except:
             context['status'] = False
             return context,  html_content
     def get_preferencias_user(self, cpf=None):
         response = {
             'esporte': [],
             'opcoes_apostas': [],
             'campeonatos':[],
             'stack_aposta':0.0
         }
         user_preferencias = list(core.cliente.models.ClientePreferencias.objects.filter(cliente_id=cpf))
         cliente_stack =core.cliente.models.Cliente.objects.values_list('stack_aposta').filter(cpf=cpf).first()[0]
         lista_preferencias_campeonatos = []
         lista_preferencias_tipo_aposta = []
         lista_preferencias_esporte = []
         for preferencia in user_preferencias:
             if preferencia.tipo_preferencia == 'campeonato':
                 lista_preferencias_campeonatos.append(preferencia.id_preferencia)
             if preferencia.tipo_preferencia == 'tipo_aposta':
                 lista_preferencias_tipo_aposta.append(preferencia.id_preferencia)
             if preferencia.tipo_preferencia == 'esporte':
                 lista_preferencias_esporte.append(preferencia.id_preferencia)
         if user_preferencias:
             response ={
                 'esporte': lista_preferencias_esporte,
                 'opcoes_apostas': lista_preferencias_tipo_aposta,
                 'opcoes_campeonatos': lista_preferencias_campeonatos,
                 'stack_aposta': cliente_stack if cliente_stack !=None else 00.00
             }
         return response

     def get_preferencias(self):
         opcoes_apostas = list(core.esporte.models.Tipo.objects.filter(tipo='OPCOES.APOSTA', status=True).values())
         esporte = list(core.esporte.models.Esporte.objects.values())
         retorno = {
             'opcoes_apostas':opcoes_apostas,
             'esporte': esporte
         }
         return retorno


     def gerar_codigo(self, email=None):
        try:
            cliente = core.cliente.models.Cliente.objects.filter(email=email).first()
            cliente.codigo_recuperacao = random.randint(100000, 999999)
            cliente.save()

            self.send_html_email(email=email, codigo=cliente.codigo_recuperacao)

            return True, ''
        except:
            return False, ''

     def logar(self):
         descricao = 'Não foi possivel logar o cliente, senha ou usuario incorretos'
         token_jwt = {}
         cliente = core.cliente.models.Cliente.objects.filter(username=self.username, status=True).first()
         if cliente is not None:
             status = cliente.check_password(raw_password=self.password)
             if status:
                 descricao = ''
                 token_jwt = self.get_token(cliente=cliente)
         else:
             status = False

         return status, descricao, token_jwt

     def get_token(self, cliente=None):
         # Definindo a chave secreta para assinar o token
         # Em produção, use uma chave secreta mais complexa e mantenha-a segura
         SECRET_KEY = 'minha_chave_secreta'

         # Informações do payload do token (os dados que você quer incluir no token, como ID do usuário, permissões, etc.)
         payload = {
             'usuario_id': 123,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # Expira em 30 minutos
             'iat': datetime.datetime.utcnow(),
             'cli_info': {'cpf':cliente.cpf,
                          'nome':cliente.nome,
                          'sobrenome':cliente.sobrenome,
                          'email':cliente.email,
                          'perfil':{'perfil_id':cliente.perfil.pk,
                                    'perfil_nm_descritivo':cliente.perfil.nm_descritivo,
                                    'perfil_nivel':cliente.perfil.nivel}
                          },
         }

         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

         # Para decodificar o token
         decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

         print(decoded_payload)

         return token



     def validar_maioridade(self, birthdate_str=None):

         # Converte a string para um objeto datetime
         birthdate = datetime.datetime.strptime(birthdate_str, "%Y%m%d")

         # Calcula a data de hoje
         today = datetime.datetime.today()

         # Calcula a diferença de anos entre a data de hoje e a data de nascimento
         age = today.year - birthdate.year

         # Ajusta a idade baseado no mês e dia
         if (today.month, today.day) < (birthdate.month, birthdate.day):
             age -= 1

         # Retorna True se a idade é 18 ou mais, caso contrário False
         return age >= 18

     def cadastrar_preferencias(self, cpf=None, esportes=[],opcoes_apostas=[], valor=None, campeonatos=[]):
         try:
             preferencias = list(core.cliente.models.ClientePreferencias.objects.filter(cliente_id=cpf))
             cliente = core.cliente.models.Cliente.objects.filter(cpf=cpf).first()
             if valor:
                cliente.stack_aposta = valor
                cliente.save()
             for pref in preferencias:
                 pref.delete()
             if esportes:
                 for esporte in esportes:
                     preferencias = core.cliente.models.ClientePreferencias()
                     preferencias.cliente_id = cpf
                     preferencias.id_preferencia = esporte
                     preferencias.tipo_preferencia = 'esporte'
                     preferencias.status = True
                     preferencias.save()
             if opcoes_apostas:
                 for opcoao_aposta in opcoes_apostas:
                     preferencias = core.cliente.models.ClientePreferencias()
                     preferencias.cliente_id = cpf
                     preferencias.id_preferencia = opcoao_aposta
                     preferencias.tipo_preferencia = 'tipo_aposta'
                     preferencias.status = True
                     preferencias.save()
             if campeonatos:
                 for campeonato in campeonatos:
                     preferencias = core.cliente.models.ClientePreferencias()
                     preferencias.cliente_id = cpf
                     preferencias.id_preferencia = campeonato
                     preferencias.tipo_preferencia = 'campeonato'
                     preferencias.status = True
                     preferencias.save()


             return True
         except:
             return False

     # def editar_preferencias(self, cpf=None, esporte=None,opcoes_apostas=None):
     #     try:
     #         preferencias = core.cliente.models.ClientePreferencias.objects.filter(cliente_id=cpf).first()
     #         preferencias.cliente_id = cpf
     #         preferencias.esporte = esporte
     #         preferencias.opcoes_apostas = opcoes_apostas
     #         preferencias.save()
     #         return True
     #     except:
     #         return False

     def cadastrar_cliente(self,nome=None,sobrenome=None,email=None,cpf=None,data_nasc=None):
         try:
             _, _, cliente_existe = self.get_cliente(cpf=Cliente.limpar_cpf(cpf))
             status_email = self.validar_email(email=email)
             status_username = self.validar_username(username=self.username)
             # status_validar_maioridade = self.validar_maioridade(birthdate_str=Cliente.limpar_data(data_nasc))
             if status_email:
                 return False, 'email já cadastrado no sistema'
             if cliente_existe:
                 return False, 'cpf já cadastrado no sistema'
             if status_username:
                 return False, 'username já está em uso no sistema'
             # if status_validar_maioridade:
             #     return False, 'cpf já cadastrado no sistema'
             cliente = core.cliente.models.Cliente()
             cliente.username = self.username
             if self.password:
                cliente.set_password(raw_password=self.password)
             cliente.email = email
             cliente.cpf = Cliente.limpar_cpf(cpf)
             cliente.nome = nome
             cliente.sobrenome = sobrenome
             cliente.data_nascimento = Cliente.limpar_data(data_nasc)
             cliente.perfil_id = 'gratuito'
             cliente.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def validar_username(self, username):
         cliente_exists = core.cliente.models.Cliente.objects.filter(username=username).exists()
         return cliente_exists

     def editar_cliente(self,nome=None,sobrenome=None,email=None,cpf=None,data_nasc=None,perfil=None):
         try:
             status_email = False
             _,_,cliente_existe = self.get_cliente(cpf=Cliente.limpar_cpf(cpf))
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
             if email != cliente_existe.get('email'):
                status_email = self.validar_email()
             if status_email:
                 return False, 'o email só pode estar vinculado a um unico usuário'
             cliente = core.cliente.models.Cliente.objects.filter(cpf=Cliente.limpar_cpf(cpf)).first()
             if self.username:
                cliente.username = self.username
             if self.password:
                cliente.set_password(raw_password=self.password)
             if email:
                cliente.email = email
             if cpf:
                cliente.cpf = Cliente.limpar_cpf(cpf)
             if nome:
                cliente.nome = nome
             if sobrenome:
                cliente.sobrenome = sobrenome
             if data_nasc:
                cliente.data_nascimento = Cliente.limpar_data(data_nasc)
             if perfil:
                cliente.perfil_id = perfil
             cliente.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def alterar_senha(self, cpf=None, old_password=None):
         try:
             cliente_existe = self.get_cliente(cpf=cpf)
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
             cliente = core.cliente.models.Cliente.objects.filter(cpf=cpf).first()
             status = cliente.check_password(raw_password=old_password)
             if status:
                 cliente.set_password(raw_password=self.password)
                 cliente.cpf = Cliente.limpar_cpf(cpf)
                 cliente.save()
             else:
                return False, 'senha antiga incorreta'
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def resetar_senha(self, codigo=None, email=None):
         try:
             cliente = core.cliente.models.Cliente.objects.filter(email=email).first()
             cliente.set_password(raw_password=self.password)
             cliente.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def verificar_codigo(self, email=None, codigo=None):
         try:
             cliente = core.cliente.models.Cliente.objects.filter(email=email).first()
             if cliente.codigo_recuperacao == int(codigo):
                cliente.set_password(raw_password=self.password)
             cliente.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def selecionar_plano(self, cpf=None, perfil_id=None):
        try:

            cliente = core.cliente.models.Cliente.objects.filter(cpf=Cliente.limpar_cpf(cpf)).first()
            if(not cliente):
                return False, 'Usuário não encontrado!'

            cliente.perfil_id = perfil_id
            cliente.save()
            return True, 'Plano selecionado com sucesso!'

        except Exception as e:
            return False, str(e)

     def deletar_cliente(self, cpf=None):
        try:
            cliente = core.cliente.models.Cliente.objects.filter(cpf=cpf).first()
            cliente.status = False
            cliente.save()
            return True, ''
        except:
            return False, 'não foi possivel deletar o cliente'

     def deletar_aposta(self, cpf=None, aposta_id=None):
         try:
             aposta = core.cliente.models.Aposta.objects.filter(cpf=cpf, id=aposta_id).first()
             aposta.status = False
             aposta.save()
             return True, ''
         except:
             return False, 'não foi possivel cancelar a aposta'


     def validar_email(self, email=None):
        try:
            email = core.cliente.models.Cliente.objects.filter(email=email).first()
            if email:
                return True
        except:
            return False

     def validar_username(self, username=None):
        try:
            email = core.cliente.models.Cliente.objects.filter(username=username).first()
            if email:
                return True
        except:
            return False
     def enviar_email(self, email=None, codigo=None):
         return



     # settings.py

     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
     EMAIL_HOST = 'smtp.gmail.com'
     EMAIL_PORT = 587
     EMAIL_USE_TLS = True
     EMAIL_HOST_USER = 'goodgainoficcial@gmail.com'
     EMAIL_HOST_PASSWORD = 'Nika@1234'

     def send_my_email(self):
         send_mail(
             'Assunto do Email',
             'Mensagem do Email. Aqui vai o corpo do email.',
             'seu_email@gmail.com',  # Email de origem
             ['t.caron@terra.com.br'],  # Lista de emails que receberão a mensagem
             fail_silently=False,
         )

     def send_html_email(self, email=None, codigo=None):
         context = {'token': codigo}
         html_content = render_to_string('email_rest_senha.html', context)

         email = EmailMessage(
             'Código de reset de senha goodgain!',
             html_content,
             'goodgainoficcial@gmail.com',
             [email]
         )
         email.content_subtype = 'html'
         email.send()

     #abaixo informações de admin
     def get_todos_usuarios(self, cpf_cliente=None):
         try:
             if cpf_cliente or self.username:
                todos_usuarios = list(core.cliente.models.Cliente.objects.filter(cpf=cpf_cliente,username=self.username))
             else:
                todos_usuarios = list(core.cliente.models.Cliente.objects.values().all())
             return todos_usuarios
         except:
             return HttpResponseServerError("Descrição do erro ou mensagem personalizada.")
