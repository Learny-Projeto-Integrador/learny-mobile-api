from api import mongo

class Pais():
    def __init__(self, foto, usuario, senha, nome, email, dataNasc, filhos, filhoSelecionado):
        self.usuario = usuario
        self.senha = senha
        self.nome = nome
        self.foto = foto
        self.email = email
        self.dataNasc = dataNasc
        self.filhos = filhos
        self.filhoSelecionado = filhoSelecionado
        
class Criancas():
    def __init__(self, foto, usuario, nome, senha, email, dataNasc, pontos, fasesConcluidas, medalhas, rankingAtual, missoesDiarias, audio, responsavel):
        self.foto = foto
        self.usuario = usuario
        self.nome = nome
        self.senha = senha
        self.email = email
        self.dataNasc = dataNasc
        self.pontos = pontos
        self.fases = fasesConcluidas,
        self.medalhas = medalhas,
        self.rankingAtual = rankingAtual
        self.missoesDiarias = missoesDiarias
        self.audio = audio
        self.responsavel = responsavel