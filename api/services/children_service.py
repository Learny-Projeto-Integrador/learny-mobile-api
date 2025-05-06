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

def register_children(data):
    foto = data.foto
    usuario = data.usuario
    nome = data.nome
    senha = generate_password_hash(data.senha)
    email = data.email
    dataNasc = data.dataNasc
    responsavel = data.responsavel
    
    if responsavel != "":
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
        'pontos': 0,
        'fasesConcluidas': 0,
        'medalhas': [],
        'rankingAtual': 0,
        'missoesDiarias': [],
        'audio': True,
        'responsavel': responsavel,
    }

    # Buscar usuário no banco
    children_data = mongo.db.criancas.find_one({'usuario': usuario})
    parent_data = mongo.db.pais.find_one({'usuario': usuario})

    if children_data or parent_data:
        return {'error': 'Usuário já existente'}
    else:
        mongo.db.criancas.insert_one(dados)
        return {'message': 'Usuário cadastrado com sucesso!'}
    
def edit_children(id, new_data):
    try:
        # Certificar que o ID é do tipo ObjectId
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}
    
    if new_data.get('senha'):
        new_data['senha'] = generate_password_hash(new_data['senha'])
    else:
        # Se não houver nova senha, remove o campo para manter a antiga
        new_data.pop('senha', None)

    result = mongo.db.criancas.update_one(
        {'_id': obj_id},
        {'$set': new_data}
    )

    if result.matched_count > 0:
        return {'message': 'Dados atualizados com sucesso'}
    else:
        return {'error': 'Pai não encontrado'}
    
def delete_children(id):
    # Buscar usuário no banco
    user_data = mongo.db.criancas.find_one({'_id': id})

    if user_data:
        mongo.db.criancas.deleteMany({'_id': id})
        return {'message': 'Conta excluida com sucesso'}
    else:
        return {'error': 'Erro ao buscar os dados da criança'}
