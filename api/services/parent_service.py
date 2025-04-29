from api import mongo
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import database
from bson import ObjectId


def get_parent_by_id(id):
    # Buscar usuário no banco
    user_data = mongo.db.pais.find_one({'_id': id})

    if user_data:
        return user_data
    else:
        return {'error': 'Erro ao buscar os dados do pai'}

def login_parent(data):
    usuario = data.get('usuario')
    senha = data.get('senha')

    # Buscar usuário no banco
    user_data = mongo.db.pais.find_one({'usuario': usuario})

    if user_data:
        if check_password_hash(user_data['senha'], senha):
            return user_data
        else:
            return {'error': 'Senha Inválida'}
    else:
        return {'error': 'Usuário ou senha inválidos'}

def register_parent(data):
    foto = data.foto
    usuario = data.usuario
    nome = data.nome
    senha = generate_password_hash(data.senha)
    email = data.email
    dataNasc = data.dataNasc

    dados = {
        'foto': foto,
        'usuario': usuario,
        'senha': senha,
        'nome': nome,
        'email': email,
        'dataNasc': dataNasc,
        'filhos': [],
    }

    # Buscar usuário no banco
    user_data = mongo.db.pais.find_one({'usuario': usuario})

    if user_data:
        return {'error': 'Usuário já existente'}
    else:
        user_data = mongo.db.pais.insert_one(dados)
        return {'message': 'Usuário cadastrado com sucesso!'}
    
def edit_parent(id, new_data):
    try:
        # Certificar que o ID é do tipo ObjectId
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    result = mongo.db.pais.update_one(
        {'_id': obj_id},
        {'$set': new_data}
    )

    if result.matched_count > 0:
        return {'message': 'Dados atualizados com sucesso'}
    else:
        return {'error': 'Pai não encontrado'}
    
def delete_parent(id):
    # Buscar usuário no banco
    user_data = mongo.db.pais.find_one({'_id': id})

    if user_data:
        mongo.db.pais.deleteMany({'_id': id})
        return {'message': 'Conta excluida com sucesso'}
    else:
        return {'error': 'Erro ao buscar os dados do pai'}
    
def add_children(id, new_child):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    result = mongo.db.pais.update_one(
        {'_id': obj_id},
        {'$push': {'filhos': new_child}}
    )

    if result.matched_count > 0:
        return {'message': 'Filho adicionado com sucesso'}
    else:
        return {'error': 'Pai não encontrado'}