from api import mongo
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import database
from bson import ObjectId, errors


def get_children_by_id(id):
    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'_id': id})

    if user_data:
        return user_data
    else:
        return {'error': 'Erro ao buscar os dados da criança'}

def login_children(data):
    usuario = data.get('usuario')
    senha = data.get('senha')

    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'usuario': usuario})

    if user_data:
        if check_password_hash(user_data['senha'], senha):
            return user_data
        else:
            return {'error': 'Senha Inválida'}
    else:
        return {'error': 'Usuário ou senha inválidos'}

def register_children(data):
    foto = data.foto
    usuario = data.usuario
    nome = data.nome
    senha = generate_password_hash(data.senha)
    email = data.email
    dataNasc = data.dataNasc
    try:
        responsavel = ObjectId(data.responsavel)
    except (errors.InvalidId, TypeError):
        return {'error': 'ID do responsável inválido.'}

    dados = {
        'foto': foto,
        'usuario': usuario,
        'senha': senha,
        'nome': nome,
        'email': email,
        'dataNasc': dataNasc,
        'responsavel': responsavel,
    }

    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'usuario': usuario})

    if user_data:
        return {'error': 'Usuário já existente'}
    else:
        user_data = mongo.db.criancas.insert_one(dados)
        return {'message': 'Usuário cadastrado com sucesso!'}
    
def delete_children(id):
    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'_id': id})

    if user_data:
        mongo.db.criancas.deleteMany({'_id': id})
        return {'message': 'Conta excluida com sucesso'}
    else:
        return {'error': 'Erro ao buscar os dados da criança'}
