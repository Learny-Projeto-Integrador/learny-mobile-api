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
    
def get_all_children(id):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    # Verifica se existe um pai com esse ID
    pai = mongo.db.pais.find_one({'_id': obj_id})
    if not pai:
        return {'error': 'Pai não encontrado ou acesso não autorizado'}

    # Busca as crianças cujo responsável é esse pai e o usuário é correspondente
    criancas = mongo.db.criancas.find({'responsavel': obj_id})
    if criancas:
        return criancas
    else:
        return {"error": "Nenhuma criança encontrada para este responsável"}

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
        'filhoSelecionado': "",
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
    
    if new_data.get('senha'):
        new_data['senha'] = generate_password_hash(new_data['senha'])
    else:
        # Se não houver nova senha, remove o campo para manter a antiga
        new_data.pop('senha', None)
        
    # Buscar usuário no banco
    parent_data = mongo.db.pais.find_one({'usuario': new_data['usuario']})
    children_data = mongo.db.criancas.find_one({'usuario': new_data['usuario']})

    if parent_data:
        result = mongo.db.pais.update_one(
            {'_id': obj_id},
            {'$set': new_data}
        )

    if children_data:
        result = mongo.db.criancas.update_one(
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

    if '_id' in new_child:
        try:
            new_child['_id'] = ObjectId(new_child['_id'])
        except Exception:
            return {'error': 'ID do filho inválido'}
        
    if pai.get('filhoSelecionado', None) == "":
        # Supondo que new_child contenha um campo "id" que deve virar ObjectId
            
        result = mongo.db.pais.update_one(
            {'_id': obj_id},
            {
                '$push': {'filhos': new_child["_id"]},
                '$set': {'filhoSelecionado': new_child["_id"]}
            }
        )
        
    else:
        result = mongo.db.pais.update_one(
            {'_id': obj_id},
            {'$push': {'filhos': new_child["_id"]}}
        )

    if result.modified_count > 0:
        return {'message': 'Filho adicionado com sucesso'}
    else:
        return {'error': 'Erro ao adicionar filho'}
    
def get_children_by_parent(id, user):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    # Verifica se existe um pai com esse ID
    pai = mongo.db.pais.find_one({'_id': obj_id})
    if not pai:
        return {'error': 'Pai não encontrado ou acesso não autorizado'}

    # Busca as crianças cujo responsável é esse pai e o usuário é correspondente
    crianca = mongo.db.criancas.find_one({'responsavel': obj_id, 'usuario': user})
    if crianca:
        return crianca
    else:
        return {"error": "Nenhuma criança encontrada para este responsável"}
    
def edit_children(id, new_child):
    print("entrou aqui")
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    # Verifica se existe um pai com esse ID
    pai = mongo.db.pais.find_one({'_id': obj_id})
    if not pai:
        return {'error': 'Pai não encontrado ou acesso não autorizado'}

    # Busca as crianças cujo responsável é esse pai e o usuário é correspondente
    crianca = list(mongo.db.criancas.find({'responsavel': obj_id, 'usuario': new_child["usuario"]}))

    if new_child['senha']:
        new_child['senha'] = generate_password_hash(new_child['senha'])
    else:
        # Se não houver nova senha, remove o campo para manter a antiga
        new_child.pop('senha', None)

    result = mongo.db.criancas.update_one(
        {'_id': crianca[0]['_id']},
        {'$set': new_child}
    )

    if result.modified_count > 0:
        return {'message': 'Filho alterado com sucesso'}
    else:
        return {'error': 'Erro ao editar o filho'}

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
            '$set': {'filhoSelecionado': new_child["_id"]}
        }
    )

    if result.modified_count > 0:
        return {'message': 'Filho selecionado alterado com sucesso'}
    else:
        return {'error': 'Erro ao alterar o filho selecionado'}
    

def delete_children_by_parent(id, user):
    try:
        obj_id = ObjectId(id)
    except Exception:
        return {'error': 'ID inválido'}

    # Verifica se existe um pai com esse ID
    pai = mongo.db.pais.find_one({'_id': obj_id})
    if not pai:
        return {'error': 'Pai não encontrado ou acesso não autorizado'}

    # Busca a criança cujo responsável é esse pai e o usuário corresponde
    crianca = mongo.db.criancas.find_one({'responsavel': obj_id, 'usuario': user})
    if not crianca:
        return {"error": "Nenhuma criança encontrada para este responsável"}

    crianca_id = crianca['_id']

    # Remove do array 'filhos' o objeto que contém o mesmo usuário
    mongo.db.pais.update_one(
        {'_id': obj_id},
        {'$pull': {'filhos': {'usuario': user}}}
    )

    # Deleta a criança da coleção
    mongo.db.criancas.delete_one({'_id': crianca_id})

    # Se o filho selecionado for o que foi removido, substituir
    filho_selecionado = pai.get('filhoSelecionado')
    if filho_selecionado and filho_selecionado.get('usuario') == user:
        # Pega o próximo filho restante desse pai (se houver)
        novo_filho = mongo.db.criancas.find_one({'responsavel': obj_id})

        if novo_filho:
            mongo.db.pais.update_one(
                {'_id': obj_id},
                {'$set': {'filhoSelecionado': novo_filho}}
            )
        else:
            # Se não houver mais filhos, remove o campo
            mongo.db.pais.update_one(
                {'_id': obj_id},
                {'$unset': {'filhoSelecionado': ""}}
            )

    return {'message': 'Conta excluída com sucesso'}