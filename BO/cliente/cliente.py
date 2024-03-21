


class Cliente():
     def __init__(self, email, password):
         self.email =  email
         self.password = password

     def get_cliente(self):
        return

     def cadastrar_cliente(self,nome_completo =None,cpf=None,data_nasc=None):
         try:
             cliente = Cliente(self.email, self.password)
             return True, ''
         except:
            return False, 'ocorreu um erro ao cadastrar o cliente'

     def logar(self):
         #aqui fica a pesquisa no banco
         if  self.email == 'teste' and  self.password =='1234':
             status = True
         else:
            status = False
         return status