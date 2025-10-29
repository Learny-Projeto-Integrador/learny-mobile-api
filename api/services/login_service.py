from api import mongo
from werkzeug.security import check_password_hash

def login(data):
    usuario = data.get('usuario')
    senha = data.get('senha')

    # Buscar usuário no banco
    parent_data = mongo.db.pais.find_one({'usuario': usuario})
    children_data = mongo.db.criancas.find_one({'usuario': usuario})

    if parent_data:
        if check_password_hash(parent_data['senha'], senha):
            parent_data['tipo'] = 'pai'
            return parent_data, 200
        else:
            return {'error': 'Senha Inválida'}
        
    elif children_data:
        if check_password_hash(children_data['senha'], senha):
            children_data['tipo'] = 'crianca'
            return children_data, 200
        else:
            return {'error': 'Senha Inválida'}, 400
    else:
        return {'error': 'Usuário ou senha inválidos'}, 400