# Importar o Flask do pacote api
from api import app, mongo
# Importando a classe Movie que está no Model
from api.models.database import Pais, Criancas
# Importando o service
from api.services import parent_service, children_service

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
            )
            parent_service.register_parent(pai)
        if 'criancas' not in mongo.db.list_collection_names():
            crianca = Criancas(
                usuario = 'joana',
                senha = '123',
                nome = 'Joana',
                foto = '',
                email = 'joana@gmail.com',
                dataNasc='01-01-2018',
                responsavel=[]
            )
            children_service.register_children(crianca)
    app.run(host="localhost", port="5000", debug=True)