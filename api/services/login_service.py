from api import mongo
from werkzeug.security import check_password_hash

def login(data):
    username = data.get('username')
    password = data.get('password')

    parent_data = mongo.db.parents.find_one({'username': username})
    children_data = mongo.db.children.find_one({'username': username})

    if parent_data:
        if check_password_hash(parent_data['password'], password):
            parent_data['type'] = 'parent'
            return parent_data, 200
        else:
            return {'error': 'Senha Inválida'}, 400
        
    elif children_data:
        if check_password_hash(children_data['password'], password):
            children_data['type'] = 'child'
            return children_data, 200
        else:
            return {'error': 'Senha Inválida'}, 400
    else:
        return {'error': 'Usuário ou senha inválidos'}, 400