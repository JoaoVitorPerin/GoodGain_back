


class Cliente():
     def __init__(self, username, password):
         self.username =  username
         self.password = password

     def get_cliente(self):
        return

     def logar(self):
         #aqui fica a pesquisa no banco
         if  self.username == 'teste' and  self.password =='1234':
             status = True
         else:
            status = False
         return status