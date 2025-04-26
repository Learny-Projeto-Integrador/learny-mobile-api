from api import mongo
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import database
from bson import ObjectId


def login_parent(parent):
    # if not parent or not parent.get('user') or not parent.get('password'):
    #     return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400

    user = parent.usuario
    password = parent.senha

    # Buscar usuário no banco
    user_data = mongo.db.pais.find_one({'usuario': user})

    if user_data:
        if check_password_hash(user_data['senha'], password):
            return jsonify({'message': 'Login realizado com sucesso!'})
        else:
            return jsonify({'error': 'Senha Inválida'}), 401
    else:
        return jsonify({'error': 'Usuário ou senha inválidos'}), 401

def register_parent(parent):
    # Lista de campos obrigatórios
    # required_fields = ['user', 'password', 'email', 'dataNasc']

    # Verifica se algum campo está ausente ou vazio
    # missing_fields = [field for field in required_fields if not parent.get(field)]

    # if missing_fields:
    #     return jsonify({'error': 'Preencha todos os campos'}), 400

    # image = parent['image']
    user = parent.usuario
    password = generate_password_hash(parent.senha)
    email = parent.email
    dataNasc = parent.dataNasc

    dados = {
        # 'foto': image,
        'usuario': user,
        'senha': password,
        'email': email,
        'dataNasc': dataNasc,
    }

    # Buscar usuário no banco
    user_data = mongo.db.pais.find_one({'usuario': user})

    if user_data:
        return jsonify({'error': 'Usuário já existente'}), 401
    else:
        user_data = mongo.db.pais.insert_one(dados)
        return jsonify({'message': 'Usuário cadastrado com sucesso!'})
