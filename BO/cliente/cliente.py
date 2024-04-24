
import core.cliente.models
import core.esporte.models
import jwt
import datetime
import random
import ast

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail



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
         if data is None:
             return ""
         return data.replace("/", "").replace("-", "")

     def get_cliente(self, cpf=None):
        try:
            cliente = core.cliente.models.Cliente.objects.values().filter(cpf=cpf).first()
            return True, '', cliente
        except:
            return False, '', {}

     def get_preferencias_user(self, cpf=None):
         response = {
             'esporte': [],
             'opcoes_apostas': []
         }
         user_preferencias = core.cliente.models.ClientePreferencias.objects.values().filter(cliente_id=cpf).first()
         if user_preferencias:
             response ={
                 'esporte': ast.literal_eval(user_preferencias.get('esporte')) if user_preferencias.get('esporte') else [],
                 'opcoes_apostas': ast.literal_eval(user_preferencias.get('opcoes_apostas')) if user_preferencias.get('opcoes_apostas') else []
             }
         return response

     def get_preferencias(self):
         opcoes_apostas = list(core.esporte.models.Tipo.objects.values().filter(tipo='OPCOES.APOSTA'))
         esporte = list(core.esporte.models.Esporte.objects.values())
         retorno = {
             'opcoes_apostas':opcoes_apostas,
             'esporte': esporte,
         }
         return retorno


     def gerar_codigo(self, email=None):
        try:
            cliente = core.cliente.models.Cliente.objects.values().filter(email=email).first()
            cliente.codigo_recuperacao = random.randint(100000, 999999)
            cliente.save()

            self.enviar_email(email=email, codigo=cliente.codigo_recuperacao)

            return True, '', cliente.codigo_recuperacao
        except:
            return False, '', 111111

     def logar(self):
         descricao = 'Não foi possivel logar o cliente, senha ou usuario incorretos'
         token_jwt = {}
         cliente = core.cliente.models.Cliente.objects.filter(username=self.username).first()
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
                          'email':cliente.email},
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

     def cadastrar_preferencias(self, cpf=None, esporte=None,opcoes_apostas=None):
         try:
             preferencias = core.cliente.models.ClientePreferencias.objects.filter(cliente_id=cpf).first()
             if not preferencias:
                preferencias = core.cliente.models.ClientePreferencias()
             preferencias.cliente_id = cpf
             preferencias.esporte = str(esporte)
             preferencias.opcoes_apostas = str(opcoes_apostas)
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
             status_validar_maioridade = self.validar_maioridade(birthdate_str=Cliente.limpar_data(data_nasc))
             if status_email:
                 return False, 'email já cadastrado no sistema'
             if cliente_existe:
                 return False, 'cpf já cadastrado no sistema'
             if status_username:
                 return False, 'cpf já cadastrado no sistema'
             if status_validar_maioridade:
                 return False, 'cpf já cadastrado no sistema'
             cliente = core.cliente.models.Cliente()
             cliente.username = self.username
             cliente.set_password(raw_password=self.password)
             cliente.email = email
             cliente.cpf = Cliente.limpar_cpf(cpf)
             cliente.nome = nome
             cliente.sobrenome = sobrenome
             cliente.data_nascimento = Cliente.limpar_data(data_nasc)
             cliente.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def validar_username(self, username):
         cliente_exists = core.cliente.models.Cliente.objects.filter(username=username).exists()
         return cliente_exists

     def editar_cliente(self,nome=None,sobrenome=None,email=None,cpf=None,data_nasc=None):
         try:
             status_email = False
             _,_,cliente_existe = self.get_cliente(cpf=cpf)
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
             if email != cliente_existe.get('email'):
                status_email = self.validar_email()
             if status_email:
                 return False, 'o email só pode estar vinculado a um unico usuário'
             cliente = core.cliente.models.Cliente.objects.filter(cpf=cpf).first()
             cliente.username = self.username
             cliente.set_password(raw_password=self.password)
             cliente.email = email
             cliente.cpf = Cliente.limpar_cpf(cpf)
             cliente.nome = nome
             cliente.sobrenome = sobrenome
             cliente.data_nascimento = Cliente.limpar_data(data_nasc)
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

     def resetar_senha(self, email=None):
         try:
             cliente = core.cliente.models.Cliente.objects.filter(email=email).first()
             cliente.set_password(raw_password=self.password)
             cliente.save()
             return True, ''
         except Exception as e:  # Captura a exceção e armazena na variável e
             print(e)  # Imprime ou faça log da exceção para ver o erro exato
             return False, str(e)  # Retorna a mensagem de erro

     def verificar_codigo(self, email=None):
         try:
             cliente = core.cliente.models.Cliente.objects.filter(email=email).first()
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

     def send_html_email(self):
         context = {'purchase': 'Livro de Django'}
         html_content = render_to_string('emails/template_email.html', context)

         email = EmailMessage(
             'Seu pedido foi realizado com sucesso!',
             html_content,
             'seu_email@gmail.com',
             ['destinatario@example.com']
         )
         email.content_subtype = 'html'
         email.send()
