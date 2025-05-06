# Importar o Flask do pacote api
from api import app, mongo
# Importando a classe Movie que está no Model
from api.models.database import Pais
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
                senha = '123',
                nome= 'João Marcos',
                foto = '',
                email = 'admin',
                dataNasc='01-01-1990',
                filhos=[],
                filhoSelecionado={},
            )
            parent_service.register_parent(pai)
    app.run(host="localhost", port="5000", debug=True)