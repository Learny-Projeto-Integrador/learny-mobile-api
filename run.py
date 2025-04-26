# Importar o Flask do pacote api
from api import app, mongo
# Importando a classe Movie que está no Model
from api.models.database import Pais, Criancas
# Importando o service
from api.services import parent_service

# Rodando a aplicação
if __name__ == "__main__":
    # Criando o banco com suas coleções
    with app.app_context():
        # Cria as coleções se não existirem
        if 'pais' not in mongo.db.list_collection_names():
            pai = Pais(
                usuario = 'admin',
                senha = 'admin',
                # foto = '',
                email = 'admin',
                dataNasc='01-01-2018'
            )
            parent_service.register_parent(pai)
        if 'criancas' not in mongo.db.list_collection_names():
            crianca = Criancas(
                usuario = 'admin',
                senha = 'admin',
                # foto = '',
                email = 'admin',
                dataNasc='01-01-2018'
            )
            parent_service.register_parent(crianca)
    app.run(host="localhost", port="5000", debug=True)