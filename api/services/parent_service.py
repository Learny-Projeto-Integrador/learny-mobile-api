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
        'filhoSelecionado': {},
    }

    # Buscar usuário no banco
    parent_data = mongo.db.pais.find_one({'usuario': usuario})
    children_data = mongo.db.criancas.find_one({'usuario': usuario})

    if parent_data or children_data:
        return {'error': 'Usuário já existente'}
    else:
        mongo.db.pais.insert_one(dados)
        return {'message': 'Usuário cadastrado com sucesso!'}
    
def edit_parent(id, new_data):
    try:
        # Certificar que o ID é do tipo ObjectId
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}
    
    # Buscar usuário no banco
    parent_data = mongo.db.pais.find_one({'usuario': new_data['usuario']})
    children_data = mongo.db.criancas.find_one({'usuario': new_data['usuario']})

    if parent_data or children_data:
        return {'error': 'Usuário já existente'}
    
    if new_data.get('senha'):
        new_data['senha'] = generate_password_hash(new_data['senha'])
    else:
        # Se não houver nova senha, remove o campo para manter a antiga
        new_data.pop('senha', None)

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
        mongo.db.pais.delete_one({'_id': id})
        return {'message': 'Conta excluida com sucesso'}
    else:
        return {'error': 'Erro ao buscar os dados do pai'}
    
def add_children(id, new_child):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    pai = mongo.db.pais.find_one({'_id': obj_id})
    if not pai:
        return {'error': 'Pai não encontrado'}

    if pai.get('filhoSelecionado', None) == {}:
        # Supondo que new_child contenha um campo "id" que deve virar ObjectId
        if '_id' in new_child:
            try:
                new_child['_id'] = ObjectId(new_child['_id'])
            except Exception:
                return {'error': 'ID do filho inválido'}
            
        result = mongo.db.pais.update_one(
            {'_id': obj_id},
            {
                '$push': {'filhos': new_child},
                '$set': {'filhoSelecionado': new_child}
            }
        )
        
    else:
        result = mongo.db.pais.update_one(
            {'_id': obj_id},
            {'$push': {'filhos': new_child}}
        )

    if result.modified_count > 0:
        return {'message': 'Filho adicionado com sucesso'}
    else:
        return {'error': 'Erro ao adicionar filho'}
    
def edit_selected_children(id, new_child):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    pai = mongo.db.pais.find_one({'_id': obj_id})
    if not pai:
        return {'error': 'Pai não encontrado'}

    if '_id' in new_child:
        try:
            new_child['_id'] = ObjectId(new_child['_id'])
        except Exception:
            return {'error': 'ID do filho inválido'}
            
    result = mongo.db.pais.update_one(
        {'_id': obj_id},
        {
            '$set': {'filhoSelecionado': new_child}
        }
    )

    if result.modified_count > 0:
        return {'message': 'Filho selecionado alterado com sucesso'}
    else:
        return {'error': 'Erro ao alterar o filho selecionado'}