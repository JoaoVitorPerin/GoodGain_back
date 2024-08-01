
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

     def get_cliente(self, cpf=None):
        try:
            cliente = core.cliente.models.Cliente.objects.values().filter(cpf=cpf).first()
            return True, '', cliente
        except:
            return False, '', {}

     def get_perfis(self):
        return list(core.cliente.models.Perfis.objects.values().filter(status=True))

     def get_apostas_cliente(self,cpf_user=None):
        try:
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
'is_aposta').filter(cliente_id=cpf_user, is_aposta=True).order_by('-id'))
            return True, lista_apostas_cliente
        except:
            return False, []

     def get_dahsboard_cliente(self, cliente_id=None):
        try:

            apostas_cliente = list(core.cliente.models.Aposta.objects.filter(cliente_id=cliente_id))
            dict_campeonatos = {}
            dict_tipo_apostas = {}
            todas_odds = 0
            valor_apostado = 0.0
            valor_anterior = 0
            tipo_aposta_mais_escolhida = 'nenhuma'
            for aposta in apostas_cliente:
                if aposta.campeonato_id not in dict_campeonatos:
                    dict_campeonatos[aposta.campeonato_id] = 1
                else:
                    dict_campeonatos[aposta.campeonato_id] = dict_campeonatos[aposta.campeonato_id] + 1
                if aposta.tipo_aposta not in dict_tipo_apostas:
                    dict_tipo_apostas[aposta.tipo_aposta] = 1
                else:
                    dict_tipo_apostas[aposta.tipo_aposta] = dict_tipo_apostas[aposta.tipo_aposta] + 1
                todas_odds+= float(aposta.odd)
                valor_apostado += aposta.valor if aposta.valor is not None else 0
            if todas_odds:
                media_odds = todas_odds/len(apostas_cliente)
            else:
                media_odds = 0.0

            if valor_apostado:
                media_valor_apostado = valor_apostado/len(apostas_cliente)
            else:
                media_valor_apostado = 0.0

            for tipo_aposta in dict_tipo_apostas:
                valor_atual = dict_tipo_apostas[tipo_aposta]
                if valor_atual > valor_anterior:
                   valor_anterior = valor_atual
                   tipo_aposta_mais_escolhida = tipo_aposta
            lista_grafico_campeonato = []
            lista_grafico_tipo = []
            for campeonato in dict_campeonatos:
                lista_grafico_campeonato.append({'campeonato': campeonato, 'valor':dict_campeonatos[campeonato]})
            for tipo_aposta in dict_tipo_apostas:
                lista_grafico_tipo.append({'tipo_aposta': tipo_aposta, 'valor': dict_tipo_apostas[tipo_aposta]})


            dados = {'status': True,
                     'qtd_apostas': len(apostas_cliente),
                     'media_odds': media_odds,
                     'valor_apostado': media_valor_apostado,
                     'tipo_aposta_mais_escolhida': tipo_aposta_mais_escolhida,
                     'grafico_campeonatos': lista_grafico_campeonato,
                     'grafico_tipo_aposta': lista_grafico_tipo}
            lista_tipos = list(core.esporte.models.Tipo.objects.values('id', 'informacao'))
            lista_campeonatos = list(core.esporte.models.Campeonato.objects.values('id', 'nome'))

            return dados, lista_tipos, lista_campeonatos
        except:
            return {'status': False}, [], []

     def vitoria_time_a(self, time_a=None, campeonato=None, evento_id=None):
         try:
            if not evento_id:
                eventos_campeonato = list(core.esporte.models.Evento.objects.filter(time_a_id=time_a,campeonato=campeonato,resultado_partida__isnull=False))
            else:
                eventos_campeonato = list(core.esporte.models.Evento.objects.filter(time_a_id=time_a, campeonato=campeonato, evento_id=evento_id,resultado_partida__isnull=False))

            vitorias = 0
            empates = 0
            if eventos_campeonato is not None:
                for evento in  eventos_campeonato:
                    resultado_partida = json.loads(evento.resultado_partida.replace("'",'"').replace('True','true').replace('False','false'))
                    if resultado_partida['home_score'] > resultado_partida['away_score']:
                        vitorias += 3
                    elif resultado_partida['home_score'] == resultado_partida['away_score']:
                        empates += 1
                    else:
                        pass


            return {'status':True,'resultado':vitorias + empates + 2}
         except:
            return {'status':True, 'resultado': 0}

     def vitoria_time_b(self, time_b=None, campeonato=None, evento_id=None):
         try:
             if not evento_id:
                 eventos_campeonato = list(
                     core.esporte.models.Evento.objects.filter(time_b_id=time_b, campeonato=campeonato,
                                                               resultado_partida__isnull=False))
             else:
                 eventos_campeonato = list(
                     core.esporte.models.Evento.objects.filter(time_b_id=time_b, campeonato=campeonato,
                                                               evento_id=evento_id, resultado_partida__isnull=False))

             vitorias = 0
             empates = 0
             if eventos_campeonato is not None:
                 for evento in eventos_campeonato:
                     resultado_partida = json.loads(
                         evento.resultado_partida.replace("'", '"').replace('True', 'true').replace('False', 'false'))
                     if resultado_partida['home_score'] > resultado_partida['away_score']:
                         vitorias += 3
                     elif resultado_partida['home_score'] == resultado_partida['away_score']:
                         empates += 1
                     else:
                         pass

             return {'status': True, 'resultado': vitorias + empates}
         except:
             return {'status': True, 'resultado': 0}

     def simular_aposta(self, casa_aposta=None, cpf_user=None, campeonato=None, time_1=None, time_2=None, odd=None,tipo_aposta=None, valor=None, is_aposta=False):
         if tipo_aposta == '1':
             dados = self.calcular_tipo_1(odd=odd, campeonato=campeonato, time_1=time_1, time_2=time_2)
         if tipo_aposta == '2':
             dados = self.vitoria_time_a(time_a=time_1, campeonato=campeonato)
             dados_b = self.vitoria_time_b(time_b=time_2, campeonato=campeonato)
             if dados.get('resultado') > dados_b.get('resultado'):
                 dados['descricao_resultado'] = 'Recomendado'
             elif dados.get('resultado') == dados_b.get('resultado'):
                 dados['descricao_resultado'] = 'Não recomendado'
             else:
                 dados['descricao_resultado'] = 'Não recomendado'
         if tipo_aposta == '3':
             dados = self.vitoria_time_b(time_b=time_2, campeonato=campeonato)
             dados_a = self.vitoria_time_a(time_a=time_1, campeonato=campeonato)
             if dados.get('resultado') > dados_a.get('resultado'):
                 dados['descricao_resultado'] = 'Recomendado'
             elif dados.get('resultado') == dados_a.get('resultado'):
                 dados['descricao_resultado'] = 'Não recomendado'
             else:
                 dados['descricao_resultado'] = 'Não recomendado'
         if dados.get('status'):
             aposta = core.cliente.models.Aposta()
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


         return dados

     def evento_simulado(self, cpf_user=None, evento=None, odd=None):
         try:
             dados = {'status':True}
             evento = core.esporte.models.Evento.objects.filter(id=evento).first()
             time_a = self.calcular_tipo_1(odd=odd, campeonato=evento.get('campeonato_id'), time_1=evento.get('time_a_id'), time_2=evento.get('time_b_id'))
             time_b = self.vitoria_time_a(campeonato=evento.get('campeonato_id'),
                                                  time_a=evento.get('time_a_id'))
             dados_25_gols = self.vitoria_time_b(campeonato=evento.get('campeonato_id'), time_b=evento.get('time_b_id'))
             if dados_25_gols.get('status'):
                 dados['dados_25_gols'] = dados_25_gols
             if time_a.get('status'):
                 dados['time_a'] = time_a
             if time_b.get('status'):
                 dados['time_b'] = time_b

             aposta = core.cliente.models.Aposta()
             aposta.cliente_id = cpf_user
             aposta.status = True
             aposta.evento_id = evento.get('id')
             aposta.campeonato_id = evento.get('campeonato_id')
             aposta.time_1_id = evento.get('time_a_id')
             aposta.time_2_id = evento.get('time_b_id')
             aposta.odd = odd
             aposta.tipo_aposta = 0
             aposta.save()

             return dados
         except:
            dados['status'] = False
            return dados

     def calcular_tipo_1(self, odd=None, campeonato=None, time_1=None, time_2=None):
         try:
             jogos_com25gols_casa_time1 = 0
             jogos_com25gols_fora_time1  = 0
             jogos_com25gols_casa_time2 = 0
             jogos_com25gols_fora_time2 = 0
             sem_dados_time1 = False
             sem_dados_time2 = False
             dict_info = {
                 'status': True,
                 'descricao': '',
                 'resultado_time_1':0,
                 'resultado_time_2':0
             }

             eventos_casa = list(core.esporte.models.Evento.objects.filter(time_a_id=time_1, resultado_partida__isnull=False))
             if eventos_casa:
                 for evento_interno in eventos_casa:
                     if json.loads(evento_interno.resultado_partida.replace("'",'"').replace('True','true').replace('False','false')).get('home_score') >=3:
                        jogos_com25gols_casa_time1 +=1
             else:
                 sem_dados_time1 = True


             eventos_fora = list(
                 core.esporte.models.Evento.objects.filter(time_b_id=time_1, resultado_partida__isnull=False))
             if eventos_fora:
                 for evento_externos in eventos_fora:
                     if json.loads(evento_externos.resultado_partida.replace("'",'"').replace('True','true').replace('False','false')).get('away_score') >=3:
                         jogos_com25gols_fora_time1 += 1
             else:
                 sem_dados_time1 = True

             eventos_casa_2 = list(
                 core.esporte.models.Evento.objects.filter(time_a_id=time_2, resultado_partida__isnull=False))
             if eventos_casa_2:
                 for evento_interno in eventos_casa_2:
                     if json.loads(evento_interno.resultado_partida.replace("'",'"').replace('True','true').replace('False','false')).get('home_score') >=3:
                         jogos_com25gols_casa_time2 += 1

             else:
                 sem_dados_time2 = True

             eventos_fora_time2 = list(
                 core.esporte.models.Evento.objects.filter(time_b_id=time_2, resultado_partida__isnull=False))
             if eventos_fora_time2:
                 for evento_externos in eventos_fora_time2:
                     if json.loads(evento_externos.resultado_partida.replace("'",'"').replace('True','true').replace('False','false')).get('away_score') >=3:
                         jogos_com25gols_fora_time2 += 1

             else:
                 sem_dados_time1 = True
             # (%de over 2.5 gols casa + %de over 2.5 gols fora) / 2 = X
             # (X / (100 / odd)) - 1 = valor da         odd
             if not sem_dados_time1:
                if jogos_com25gols_casa_time1 != 0:
                    perc_over25_casa_time1 = jogos_com25gols_casa_time1/len(eventos_casa)
                else:
                    perc_over25_casa_time1 = 0
                if jogos_com25gols_fora_time1 != 0:
                    perc_over25_fora_time1 = jogos_com25gols_fora_time1/len(eventos_fora)
                else:
                    perc_over25_fora_time1 = 0
                x_time1 = (perc_over25_casa_time1 + perc_over25_fora_time1) / 2
                resultado_time_1 = (x_time1 / (100 / float(odd))) - 1
                dict_info['resultado_time_1'] = resultado_time_1

             if not sem_dados_time2:
                 if jogos_com25gols_casa_time2 != 0:
                     perc_over25_casa_time2 = jogos_com25gols_casa_time2 / len(eventos_casa_2)
                 else:
                     perc_over25_casa_time2 = 0
                 if jogos_com25gols_fora_time2 != 0:
                     perc_over25_fora_time2 = jogos_com25gols_fora_time2 / len(eventos_fora_time2)
                 else:
                    perc_over25_fora_time2 = 0
                 x_time2 = (perc_over25_casa_time2 + perc_over25_fora_time2) / 2
                 resultado_time_2 = (x_time2 / (100 / float(odd))) - 1
                 dict_info['resultado_time_2'] = resultado_time_2


             return dict_info
         except:
             dict_info['status'] = False
             dict_info['descricao'] = 'não foi possivel gerar a simulação'
             return dict_info
     def get_preferencias_user(self, cpf=None):
         response = {
             'esporte': [],
             'opcoes_apostas': [],
             'stack_aposta':0.0
         }
         user_preferencias = core.cliente.models.ClientePreferencias.objects.values().filter(cliente_id=cpf).first()
         if user_preferencias:
             response ={
                 'esporte': ast.literal_eval(user_preferencias.get('esporte')) if user_preferencias.get('esporte') else [],
                 'opcoes_apostas': ast.literal_eval(user_preferencias.get('opcoes_apostas')) if user_preferencias.get('opcoes_apostas') else [],
                 'stack_aposta': user_preferencias.get('stack_aposta')
             }
         return response

     def get_preferencias(self):
         opcoes_apostas = list(core.esporte.models.Tipo.objects.values().filter(tipo='OPCOES.APOSTA'))
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

     def cadastrar_preferencias(self, cpf=None, esporte=None,opcoes_apostas=None, valor=None):
         try:
             preferencias = core.cliente.models.ClientePreferencias.objects.filter(cliente_id=cpf).first()
             if not preferencias:
                preferencias = core.cliente.models.ClientePreferencias()
             preferencias.cliente_id = cpf
             preferencias.esporte = str(esporte)
             preferencias.opcoes_apostas = str(opcoes_apostas)
             preferencias.status = True
             preferencias.stack_aposta = valor
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
             cliente.username = self.username
             cliente.set_password(raw_password=self.password)
             cliente.email = email
             cliente.cpf = Cliente.limpar_cpf(cpf)
             cliente.nome = nome
             cliente.sobrenome = sobrenome
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

     def deletar_cliente(self, cpf=None):
        try:
            cliente = core.cliente.models.Cliente.objects.filter(cpf=cpf).first()
            cliente.status = False
            cliente.save()
            return True, ''
        except:
            return False, 'não foi possivel deletar o cliente'


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
             if not cpf_cliente or not self.username:
                todos_usuarios = list(core.cliente.models.Cliente.objects.filter(cpf=cpf_cliente,username=self.username))
             else:
                todos_usuarios = list(core.cliente.models.Cliente.objects.all())
             return True, todos_usuarios
         except:
             return False, []
