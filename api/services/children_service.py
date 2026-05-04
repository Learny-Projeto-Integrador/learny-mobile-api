from api import mongo
from pymongo import DESCENDING
from api.services.game_progress_service import check_and_unlock_medals, check_missions, create_activity, update_progress
from api.services.base_service import convert_id, mongo_to_dict
        
def get_child_by_id(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    child = mongo.db.children.find_one({'_id': child_oid})
    if child:
        child = mongo_to_dict(child)
        return child, 200
    else:
        return {"error": "Nenhum filho selecionado"}, 404
    
def edit_child(id, new_data):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    result = mongo.db.children.update_one(
        {'_id': child_oid},
        {'$set': new_data}
    )

    if result.matched_count == 0:
        return {'error': 'Criança não encontrada'}, 404

    if result.modified_count == 0:
        return {
            'message': 'Nenhuma alteração realizada — os dados enviados são iguais aos existentes.'
        }, 200

    return {'message': 'Dados alterados com sucesso'}, 200
    
def get_child_progress(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    progress = mongo.db.progress.find_one({"child": child_oid})

    if not progress:
        return {"error": "Não há progresso registrado para esta criança"}, 404

    return progress, 200

def get_ranking():
    ranking_cursor = mongo.db.progress.aggregate([
        {
            "$lookup": {
                "from": "children",
                "localField": "child",
                "foreignField": "_id",
                "as": "childData"
            }
        },
        {
            "$unwind": "$childData"
        },
        {
            "$sort": { "points": -1 }
        }
    ])

    ranking = []
    
    for c in ranking_cursor:
        ranking.append({
            "id": str(c["childData"]["_id"]),
            "profilePicture": c["childData"].get("profilePicture", ""),
            "name": c["childData"].get("name", ""),
            "points": c.get("points", 0)
        })

    if not ranking:
        return {'error': 'Dados das crianças não encontrados'}, 404

    return ranking
    
def edit_rankings():
    criancas = list(mongo.db.children.find().sort('points', -1))

    for index, crianca in enumerate(criancas):
        mongo.db.children.update_one(
            {'_id': crianca['_id']},
            {'$set': {'ranking': index + 1}}
        )
   
def complete_phase(child_id, phase_code, world_code):
    child_oid = convert_id(child_id)
    if not child_oid:
        return {"error": "ID inválido"}, 400

    child = mongo.db.children.find_one({"_id": child_oid})
    if not child:
        return {"error": "Criança não encontrada"}, 404

    # 1. Pontos base
    points_earned = 10

    # 2. Atualizar progresso
    update_progress(child_oid, world_code, phase_code, points_earned)

    # 3. Verificar medalhas
    medals = check_and_unlock_medals(child_oid, world_code)

    # 4. Verificar missões
    mission_result, bonus = check_missions(child_oid, phase_code)

    # 5. Log de atividade
    create_activity(child_oid, "phase_completed", {
        "phaseCode": phase_code,
        "worldCode": world_code
    })

    # bônus
    if bonus:
        mongo.db.progress.update_one(
            {"child": child_oid},
            {"$inc": {"points": bonus}}
        )

    updated_child = mongo.db.children.find_one({"_id": child_oid})

    return {
        "message": "Fase concluída com sucesso",
        "pointsEarned": points_earned + bonus,
        "medalsUnlocked": medals,
        "mission": mission_result,
        "child": mongo_to_dict(updated_child)
    }, 200
