from api import mongo

class Pais():
    def __init__(self, foto, usuario, senha, nome, email, dataNasc, filhos):
        self.usuario = usuario
        self.senha = senha
        self.nome = nome
        self.foto = foto
        self.email = email
        self.dataNasc = dataNasc
        self.filhos = filhos
        
class Criancas():
    def __init__(self, foto, usuario, nome, senha, email, dataNasc, responsavel):
        self.foto = foto
        self.usuario = usuario
        self.nome = nome
        self.senha = senha
        self.email = email
        self.dataNasc = dataNasc
        self.responsavel = responsavel