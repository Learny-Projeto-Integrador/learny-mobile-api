from api import mongo

def insert_medals():
    medalhas = [
        {
            "nome": "Iniciando!",
            "descricao": "Você concluiu a fase 01",
            "mundo": 1
        },
        {
            "nome": "A todo o vapor!",
            "descricao": "Você concluiu 3 fases",
            "mundo": 1
        },
        {
            "nome": "Desvendando",
            "descricao": "Você concluiu o mundo 01",
            "mundo": 1
        },
    ]
    mongo.db.medalhas.insert_many(medalhas)

def insert_missions():
    missoes = [
         {
            "nome": "Iniciando!",
            "descricao": "Conclua a fase 01",
            "mundo": 1
        },
        {
            "nome": "A todo o vapor!",
            "descricao": "Conclua 3 fases",
            "mundo": 1
        },
        {
            "nome": "Desvendando",
            "descricao": "Conclua o mundo 01",
            "mundo": 1
        },
    ]
    mongo.db.missoes.insert_many(missoes)
    

def insert_daily_missions():
    missoesDiarias = [         
        {
            "nome": "fase connect",
            "descricao": "Conclua a fase de ligar"
        },
        {
            "nome": "fase feeling",
            "descricao": "Conclua a fase de emoções"
        },
        {
            "nome": "fase listening",
            "descricao": "Conclua a fase de escuta"
        },
        ]
    
    mongo.db.diarias.insert_many(missoesDiarias)

def insert_data():
    insert_medals()
    insert_missions()
    insert_daily_missions()
    



