from api import mongo
from werkzeug.security import generate_password_hash
from api.models import child
from api.models.game import Progress
from api.services.base_service import convert_id, mongo_to_dict
from ..models import parent

def get_parent_by_id(id):
    user_data = mongo.db.parents.find_one({'_id': id})

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
    user_data = mongo.db.parents.find_one({'_id': id})

    if user_data:
        mongo.db.parents.delete_one({'_id': id})
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

    pai = mongo.db.parents.find_one({'_id': parent_oid})
    if not pai:
        return {'error': 'Responsável não encontrado'}, 404

    crianca = mongo.db.children.find_one({'_id': pai.get("selectedChild")})
    if crianca:
        crianca = mongo_to_dict(crianca)
        return crianca, 200
    else:
        return {"error": "Nenhum filho selecionado"}, 404
    
def create_initial_progress(child_id):
    worlds_def = list(mongo.db.world_definitions.find().sort("order", 1))

    worlds_progress = []

    for index, world in enumerate(worlds_def):
        worlds_progress.append({
            "worldCode": world["code"],
            "percentage": 0.0,
            "completedPhases": [],
            "unlocked": index == 0  # 🔥 só o primeiro desbloqueado
        })

    progress = Progress(
        child=child_id,
        worlds=worlds_progress,
        dailyMissions=[],
        medals=[],
    )

    return progress.to_dict()

def register_children(parent_id, child):
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
        {"_id": parent_oid, "selectedChild": None},
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
    
def edit_child_status(id, new_data):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    result = mongo.db.children.update_one(
        {'_id': child_oid},
        {'$set': new_data}
    )

    if result.modified_count > 0:
        return {'message': 'Status do filho alterado com sucesso'}, 200
    else:
        return {'error': 'Erro ao editar o status filho'}, 500
    
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

def edit_selected_children(parent_id, child_id):
    parent_oid = convert_id(parent_id)
    child_oid = convert_id(child_id)

    mongo.db.parents.update_one(
        {"_id": parent_oid},
        {"$set": {"selectedChild": child_oid}}
    )

    child = mongo.db.children.find_one({"_id": child_oid})

    return mongo_to_dict(child), 200