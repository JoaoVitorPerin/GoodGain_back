
import core.cliente.models
import jwt
import datetime


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail

class Cliente():
     def __init__(self, username=None, password=None):
         self.username = username
         self.password = password

     @staticmethod
     def limpar_cpf(cpf):
         return cpf.replace(".", "").replace("-", "")

     @staticmethod
     def limpar_data(cpf):
         return cpf.replace("/", "").replace("-", "")

     def get_cliente(self, cpf=None):
        try:
            cliente = core.cliente.models.Cliente.objects.values().filter(cpf=cpf).first()
            return True, '', cliente
        except:
            return False, '', {}

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
     def cadastrar_cliente(self,nome=None,sobrenome=None,email=None,cpf=None,data_nasc=None):
         try:
             _, _, cliente_existe = self.get_cliente(cpf=cpf)
             status_email = self.validar_email()
             if status_email:
                 return False, 'email já cadastrado no sistema'
             if cliente_existe:
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

     def editar_cliente(self,nome=None,sobrenome=None,email=None,cpf=None,data_nasc=None):
         try:
             cliente_existe = self.get_cliente(cpf=cpf)
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
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

     def alterar_senha(self, cpf=None):
         try:
             cliente_existe = self.get_cliente(cpf=cpf)
             if not cliente_existe:
                 return False, 'cpf não encontrado no sistema'
             cliente = core.cliente.models.Cliente.objects.filter(cpf=cpf).first()
             cliente.set_password(raw_password=self.password)
             cliente.cpf = Cliente.limpar_cpf(cpf)
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

     def enviar_email(self, email=None):
         return



     # settings.py

     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
     EMAIL_HOST = 'smtp.gmail.com'
     EMAIL_PORT = 587
     EMAIL_USE_TLS = True
     EMAIL_HOST_USER = 'seu_email@gmail.com'
     EMAIL_HOST_PASSWORD = 'sua_senha'

     def send_my_email(self):
         send_mail(
             'Assunto do Email',
             'Mensagem do Email. Aqui vai o corpo do email.',
             'seu_email@gmail.com',  # Email de origem
             ['destinatario@example.com'],  # Lista de emails que receberão a mensagem
             fail_silently=False,
         )

     def send_html_email(self):
         context = {'username': 'Fulano', 'purchase': 'Livro de Django'}
         html_content = render_to_string('emails/template_email.html', context)

         email = EmailMessage(
             'Seu pedido foi realizado com sucesso!',
             html_content,
             'seu_email@gmail.com',
             ['destinatario@example.com']
         )
         email.content_subtype = 'html'
         email.send()
