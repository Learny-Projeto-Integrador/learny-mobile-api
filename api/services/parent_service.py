from datetime import datetime

from api import mongo
from werkzeug.security import generate_password_hash
from api.models import child
from api.models.game import Progress
from api.services.base_service import convert_id, mongo_to_dict
from ..models import parent

def get_parent_by_id(id):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400
    
    user_data = mongo.db.parents.find_one({'_id': parent_oid})

    if user_data:
        return user_data, 200
    else:
        return {'error': 'Responsável não encontrado'}, 404

def register_parent(parent: parent.Parent):
    if mongo.db.parents.find_one({'username': parent.username}):
        return {'error': 'Usuário já existente'}, 400

    parent.password = generate_password_hash(parent.password)

    mongo.db.parents.insert_one(parent.to_dict())

    return {'message': 'Usuário cadastrado com sucesso!'}, 201
    
def edit_parent(id, new_data: parent.Parent):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    if new_data.password:
        new_data.password = generate_password_hash(new_data.password)

    result = mongo.db.parents.update_one({'_id': parent_oid}, {'$set': new_data.to_dict()})

    if result.matched_count > 0:
        return {'message': 'Dados atualizados com sucesso'}, 200
    else:
        return {'error': 'Responsável não encontrado'}, 404

def delete_parent(id):
    parent_oid = convert_id(id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    user_data = mongo.db.parents.find_one({'_id': parent_oid})

    if user_data:
        mongo.db.parents.delete_one({'_id': parent_oid})
        return {'message': 'Conta excluida com sucesso'}, 200
    else:
        return {'error': 'Responsável não encontrado'}, 404
    
def get_all_children(parent_id):
    parent_oid = convert_id(parent_id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    children = list(mongo.db.children.find({'parent': parent_oid}))

    return mongo_to_dict(children), 200
    
def get_child_by_id(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    crianca = mongo.db.children.find_one({'_id': child_oid})
    if crianca:
        crianca = mongo_to_dict(crianca)
        return crianca, 200
    else:
        return {"error": "Nenhum filho selecionado"}, 404
    
def get_selected_child(id):
    parent_oid = convert_id(id)

    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    parent = mongo.db.parents.find_one({
        '_id': parent_oid
    })

    if not parent:
        return {'error': 'Responsável não encontrado'}, 404

    selected_child = parent.get("selectedChild")

    if not selected_child:
        return {
            "error": "Nenhum filho selecionado"
        }, 404

    child = mongo.db.children.find_one({
        '_id': selected_child
    })

    if not child:
        return {
            "error": "Filho não encontrado"
        }, 404

    child_progress = mongo.db.progress.find_one({
        'child': selected_child
    })

    # -----------------------------------
    # SERIALIZA
    # -----------------------------------

    child_data = mongo_to_dict(child)

    progress_data = (
        mongo_to_dict(child_progress)
        if child_progress
        else {}
    )

    # -----------------------------------
    # REMOVE CAMPOS DESNECESSÁRIOS
    # -----------------------------------

    progress_data.pop("_id", None)

    progress_data.pop("child", None)

    # -----------------------------------
    # MERGE
    # -----------------------------------

    merged_data = {
        **child_data,
        **progress_data
    }

    return merged_data, 200
    
def create_initial_progress(child_id):
    worlds_def = list(mongo.db.world_definitions.find().sort("order", 1))

    worlds_progress = []

    for index, world in enumerate(worlds_def):
        worlds_progress.append({
            "worldCode": world["code"],
            "percentage": 0.0,
            "completedPhases": [],
            "unlocked": index == 0
        })

    progress = Progress(
        child=child_id,
        worlds=worlds_progress,
        dailyMissions=[],
        streak=0,
        characters=[],
        stellarPoints=0,
        coins=0,
        selectedCharacter=None
    )

    return progress.to_dict()

def register_child(parent_id, child):
    parent_oid = convert_id(parent_id)
    if not parent_oid:
        return {'error': 'ID inválido'}, 400

    if mongo.db.children.find_one({'username': child.username}):
        return {'error': 'Usuário já existente'}, 400

    child.password = generate_password_hash(child.password)
    child.parent = parent_oid

    result = mongo.db.children.insert_one(child.to_dict())
    child_id = result.inserted_id

    # ✅ cria progresso inicial
    progress_doc = create_initial_progress(child_id)
    mongo.db.progress.insert_one(progress_doc)

    # opcional: definir filho selecionado se não existir
    mongo.db.parents.update_one(
        {"_id": parent_oid, "selectedChild": None or ""},
        {"$set": {"selectedChild": result.inserted_id}}
    )

    return {'message': 'Filho criado com sucesso'}, 201
    
def edit_child(id, new_data: child.Child):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    if new_data.password:
        new_data.password = generate_password_hash(new_data.password)

    result = mongo.db.children.update_one(
        {'_id': child_oid},
        {'$set': new_data.to_dict()}
    )

    if result.modified_count > 0:
        return {'message': 'Filho alterado com sucesso'}, 200
    else:
        return {'error': 'Erro ao editar o filho'}, 500
    
def delete_child(child_id, parent_id):
    child_oid = convert_id(child_id)
    parent_oid = convert_id(parent_id)

    if not child_oid or not parent_oid:
        return {'error': 'ID inválido'}, 400

    child = mongo.db.children.find_one({
        "_id": child_oid,
        "parent": parent_oid
    })

    if not child:
        return {"error": "Não encontrado"}, 404

    mongo.db.children.delete_one({"_id": child_oid})

    return {"message": "Filho removido"}, 200

def get_child_activity(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    activity = mongo.db.activities.find({"child": child_oid})

    if not activity:
        return {"error": "Não há progresso registrado para esta criança"}, 404

    return activity, 200

def edit_selected_children(parent_id, child_id):
    parent_oid = convert_id(parent_id)
    child_oid = convert_id(child_id)

    mongo.db.parents.update_one(
        {"_id": parent_oid},
        {"$set": {"selectedChild": child_oid}}
    )

    child = mongo.db.children.find_one({"_id": child_oid})

    return mongo_to_dict(child), 200

def send_notification(child_id, parent_id, data):
    child_oid = convert_id(child_id)
    parent_oid = convert_id(parent_id)

    if not child_oid:
        return {"error": "ID da criança inválido"}, 400
    
    if not parent_oid:
        return {"error": "ID do responsável inválido"}, 400

    child = mongo.db.children.find_one({"_id": child_oid})
    parent = mongo.db.parents.find_one({"_id": parent_oid})

    if not child:
        return {"error": "Criança não encontrada"}, 404
    
    if not parent:
        return {"error": "Responsável não encontrado"}, 404
    
    if not data.get("type"):
        return { "error": "Informe o tipo de notificação" }, 400
    
    if not data.get("phaseCode"):
        return { "error": "Código da fase não informado" }, 400

    mongo.db.notifications.insert_one({
        "child": child_oid,
        "parent": {
            "_id": parent_oid,
            "name": parent["name"]
        },
        "phaseCode": data.get("phaseCode"),
        "type": data.get("type"),
        "description": data.get("description"),
        "createdAt": datetime.now()
    })
    
    return {
        "message": "Notificação registrada com sucesso",
    }, 200