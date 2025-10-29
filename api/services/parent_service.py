from api import mongo
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..models import database
from bson import ObjectId

def get_parent_by_id(id):
    user_data = mongo.db.pais.find_one({'_id': id})

    if user_data:
        return user_data, 200
    else:
        return {'error': 'Responsável não encontrado'}, 404

def register_parent(parent: database.Pai):
    if mongo.db.criancas.find_one({'usuario': parent.usuario}) or mongo.db.pais.find_one({'usuario': parent.usuario}):
        return {'error': 'Usuário já existente'}, 400
    
    if parent.senha:
        parent.senha = generate_password_hash(parent.senha)
    else:
        return {'error': 'Digite a senha'}, 400

    mongo.db.pais.insert_one(parent.to_dict())
    return {'message': 'Usuário cadastrado com sucesso!'}, 201
    
def edit_parent(id, new_data: database.Pai):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    if new_data.senha:
        new_data.senha = generate_password_hash(new_data.senha)

    result = mongo.db.pais.update_one({'_id': parent_oid}, {'$set': new_data.to_dict()})

    if result.matched_count > 0:
        return {'message': 'Dados atualizados com sucesso'}, 200
    else:
        return {'error': 'Responsável não encontrado'}, 404

def delete_parent(id):
    user_data = mongo.db.pais.find_one({'_id': id})

    if user_data:
        mongo.db.pais.delete_one({'_id': id})
        return {'message': 'Conta excluida com sucesso'}, 200
    else:
        return {'error': 'Responsável não encontrado'}, 404
    
def get_all_children(id):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    pai = mongo.db.pais.find_one({'_id': parent_oid})
    if not pai:
        return {'error': 'Responsável não encontrado'}, 404

    criancas = list(mongo.db.criancas.find({'responsavel': parent_oid}))
    if criancas:
        criancas = mongo_to_dict(criancas)
        return criancas, 200
    else:
        return {"error": "Nenhuma criança encontrada para este responsável"}, 404
    
def get_child_by_id(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    crianca = mongo.db.criancas.find_one({'_id': child_oid})
    if crianca:
        crianca = mongo_to_dict(crianca)
        return crianca, 200
    else:
        return {"error": "Nenhum filho selecionado"}, 404
    
def get_selected_child(id):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    pai = mongo.db.pais.find_one({'_id': parent_oid})
    if not pai:
        return {'error': 'Responsável não encontrado'}, 404

    crianca = mongo.db.criancas.find_one({'_id': pai.get("filhoSelecionado")})
    if crianca:
        crianca = mongo_to_dict(crianca)
        return crianca, 200
    else:
        return {"error": "Nenhum filho selecionado"}, 404
    
def register_children(id: str, child: database.Crianca):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    pai = mongo.db.pais.find_one({'_id': parent_oid})
    if not pai:
        return {'error': 'Responsável não encontrado'}, 404

    if mongo.db.criancas.find_one({'usuario': child.usuario}) or mongo.db.pais.find_one({'usuario': child.usuario}):
        return {'error': 'Usuário já existente'}, 400

    missoes = list(mongo.db.diarias.aggregate([{ "$sample": { "size": 3 } }]))
    for m in missoes:
        m.pop('_id', None)

    if child.senha:
        child.senha = generate_password_hash(child.senha)
    else:
        return {'error': 'Digite a senha'}, 400
    
    child.missoesDiarias = missoes
    child.mundos = [{
        "mundo": 1,
        "faseAtual": "",
        "fases": [{"fase": i, "concluida": False} for i in range(1, 4)] + [{"boss": 4, "concluida": False}]
    }]
    child.responsavel = parent_oid

    result = mongo.db.criancas.insert_one(child.to_dict())

    update_data = {'$push': {'filhos': result.inserted_id}}
    if not pai.get('filhoSelecionado'):
        update_data['$set'] = {'filhoSelecionado': result.inserted_id}

    mongo.db.pais.update_one({'_id': parent_oid}, update_data)
    return {'message': 'Filho adicionado com sucesso'}, 201
    
def edit_child(id, new_data: database.Crianca):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    if new_data.senha:
        new_data.senha = generate_password_hash(new_data.senha)

    result = mongo.db.criancas.update_one(
        {'_id': child_oid},
        {'$set': new_data.to_dict()}
    )

    if result.modified_count > 0:
        return {'message': 'Filho alterado com sucesso'}, 200
    else:
        return {'error': 'Erro ao editar o filho'}, 500
    
def edit_child_status(id, new_data):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    result = mongo.db.criancas.update_one(
        {'_id': child_oid},
        {'$set': new_data}
    )

    if result.modified_count > 0:
        return {'message': 'Status do filho alterado com sucesso'}, 200
    else:
        return {'error': 'Erro ao editar o status filho'}, 500
    
def delete_child(id, parent_id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID do filho inválido'}, 400
    
    parent_oid = convert_id(parent_id)
    if not parent_oid:
        return {'error': 'ID do pai inválido'}, 400
    
    # Verifica se existe um pai com esse ID
    pai = mongo.db.pais.find_one({'_id': parent_oid})
    if not pai:
        return {'error': 'Pai não encontrado ou acesso não autorizado'}, 404

    # Busca a criança cujo responsável é esse pai
    crianca = mongo.db.criancas.find_one({'_id': child_oid, 'responsavel': parent_oid})
    if not crianca:
        return {"error": "Nenhuma criança encontrada para este responsável"}, 404

    # Remove o ObjectId do array 'filhos'
    mongo.db.pais.update_one(
        {'_id': parent_oid},
        {'$pull': {'filhos': child_oid}}
    )

    # Deleta a criança da coleção
    mongo.db.criancas.delete_one({'_id': child_oid})

    # Se o filho selecionado for o que foi removido, substituir
    if pai.get('filhoSelecionado') == child_oid:
        # Pega o próximo filho restante desse pai (se houver)
        novo_filho = mongo.db.criancas.find_one({'responsavel': parent_oid})

        if novo_filho:
            mongo.db.pais.update_one(
                {'_id': parent_oid},
                {'$set': {'filhoSelecionado': novo_filho['_id']}}
            )
        else:
            # Se não houver mais filhos, remove o campo
            mongo.db.pais.update_one(
                {'_id': parent_oid},
                {'$unset': {'filhoSelecionado': ""}}
            )

    return {'message': 'Conta excluída com sucesso'}, 204

def edit_selected_children(id, child_id):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400
    
    child_oid = convert_id(child_id)
    if not child_oid:
        return {'error': 'ID do filho inválido'}, 400

    pai = mongo.db.pais.find_one({'_id': parent_oid})
    if not pai:
        return {'error': 'Pai não encontrado'}, 404
            
    result = mongo.db.pais.update_one(
        {'_id': parent_oid},
        {
            '$set': {'filhoSelecionado': child_oid}
        }
    )

    if result.modified_count > 0:
        crianca = mongo.db.criancas.find_one({'_id': child_oid})
        if crianca:
            crianca = mongo_to_dict(crianca)
            return crianca, 200
    else:
        return {'error': 'Erro ao alterar o filho selecionado'}, 500
    
def convert_id(id_str):
    try:
        return ObjectId(id_str)
    except Exception:
        return None
    
def mongo_to_dict(doc):
    if isinstance(doc, list):
        return [mongo_to_dict(item) for item in doc]
    elif isinstance(doc, dict):
        new_doc = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                new_doc[key] = str(value)
            elif isinstance(value, (dict, list)):
                new_doc[key] = mongo_to_dict(value)
            else:
                new_doc[key] = value
        return new_doc
    else:
        return doc