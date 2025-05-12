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
    def __init__(self, foto, avatar, usuario, nome, senha, email, dataNasc, pontos, fasesConcluidas, medalhas, medalhaSelecionada, rankingAtual, missoesDiarias, audio, mundos, responsavel):
        self.foto = foto
        self.avatar = avatar
        self.usuario = usuario
        self.nome = nome
        self.senha = senha
        self.email = email
        self.dataNasc = dataNasc
        self.pontos = pontos
        self.fases = fasesConcluidas,
        self.medalhas = medalhas,
        self.medalhaSelecionada = medalhaSelecionada,
        self.rankingAtual = rankingAtual
        self.missoesDiarias = missoesDiarias
        self.audio = audio
        self.mundos = mundos
        self.responsavel = responsavel
    