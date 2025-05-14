# Importar o Flask do pacote api
from api import app, mongo
# Importando o service
from api.services import base_data_service

# Rodando a aplicação
if __name__ == "__main__":
    # Criando o banco com suas coleções
    with app.app_context():
        required_collections = ['pais', 'medalhas', 'missoes', 'diarias']
        existing_collections = mongo.db.list_collection_names()

        # Se alguma coleção obrigatória não existir, insere os dados
        if not all(col in existing_collections for col in required_collections):
            base_data_service.insert_data()

    app.run(host="localhost", port="5000")