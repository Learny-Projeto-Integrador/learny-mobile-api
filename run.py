# Importar o Flask do pacote api
from api import app, mongo
# Importando o service
from api.services import base_data_service

@app.route("/")
def home():
    return "API está rodando 🚀"

# Criando o banco com suas coleções iniciais, se não existirem
with app.app_context():
    required_collections = ['pais', 'medalhas', 'missoes', 'diarias']
    existing_collections = mongo.db.list_collection_names()

    # Se alguma coleção obrigatória não existir, insere os dados
    if not all(col in existing_collections for col in required_collections):
        base_data_service.insert_data()

if __name__ == "__main__":
    app.run(host="localhost", debug=True)