
import core.cliente.models
import jwt
import datetime


class Cliente():
     def __init__(self, username, password):
         self.username =  username
         self.password = password

     @staticmethod
     def limpar_cpf(cpf):
         return cpf.replace(".", "").replace("-", "")

     @staticmethod
     def limpar_data(cpf):
         return cpf.replace("/", "").replace("-", "")

     def get_cliente(self):
        return

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