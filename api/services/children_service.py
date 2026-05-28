from api import mongo
from api.services.game_progress_service import check_missions, create_activity, update_progress
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

def edit_child_progress(id, new_data):
    child_oid = convert_id(id)

    if not child_oid:
        return {"error": "ID inválido"}, 400

    progress = mongo.db.progress.find_one({
        "child": child_oid
    })

    if not progress:
        return {"error": "Progresso não encontrado"}, 404

    # -----------------------------------
    # CAMPOS INCREMENTÁVEIS
    # -----------------------------------

    incrementable_fields = [
        "coins",
        "stellarPoints",
        "points",
        "streak"
    ]

    inc_data = {}

    for field in incrementable_fields:
        if field in new_data:
            inc_data[field] = int(new_data[field])

    # -----------------------------------
    # VALIDAÇÃO DE COINS
    # -----------------------------------

    if "coins" in inc_data:
        coins_change = inc_data["coins"]

        if coins_change < 0:
            coins_cost = abs(coins_change)

            if progress.get("coins", 0) < coins_cost:
                return {
                    "error": "Coins insuficientes"
                }, 400
       
    # -----------------------------------
    # VALIDAÇÃO DE STELLAR POINTS
    # -----------------------------------
                
    if "stellarPoints" in inc_data:
        stellar_change = inc_data["stellarPoints"]

        if stellar_change < 0:
            stellar_cost = abs(stellar_change)

            if progress.get("stellarPoints", 0) < stellar_cost:
                return {
                    "error": "Stellar Points insuficientes"
                }, 400

    # -----------------------------------
    # CAMPOS NORMAIS
    # -----------------------------------

    allowed_set_fields = [
        "selectedCharacter"
    ]
    
    set_data = {}

    for key, value in new_data.items():
        if key in allowed_set_fields:
            set_data[key] = value
            
    upgrade_character = new_data.get("upgradeCharacter")

    if upgrade_character:

        character = next(
            (
                char
                for char in progress.get("characters", [])
                if char.get("characterCode") == upgrade_character
            ),
            None
        )

        if not character:
            return {
                "error": "Personagem não encontrado"
            }, 404

        current_level = character.get("level", 1)

        current_points = character.get(
            "characterPoints",
            0
        )

        required_points = int(
            80 + 45 * ((current_level - 1) ** 1.4)
        )

        if current_points < required_points:
            return {
                "error": "Progresso insuficiente"
            }, 400

    # -----------------------------------
    # MONTA UPDATE
    # -----------------------------------

    update_query = {}

    if inc_data:
        update_query["$inc"] = inc_data

    if set_data:
        update_query["$set"] = set_data

    if not update_query:
        return {
            "error": "Nenhum dado válido enviado"
        }, 400

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    result = mongo.db.progress.update_one(
        {"child": child_oid},
        update_query
    )
    
    if upgrade_character:

        mongo.db.progress.update_one(
            {
                "child": child_oid,
                "characters.characterCode": upgrade_character
            },
            {
                "$inc": {
                    "characters.$.level": 1
                },
                "$set": {
                    "characters.$.characterPoints": 0
                }
            }
        )

    if result.matched_count == 0:
        return {
            "error": "Dados de progresso não encontrados"
        }, 404

    return {
        "message": "Dados alterados com sucesso"
    }, 200
    
def get_child_progress(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400
    
    progress = mongo.db.progress.find_one({"child": child_oid})

    if not progress:
        print("deu 404 pq nao encontrou")
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
   
from datetime import datetime

def complete_phase(child_id, data):
    child_oid = convert_id(child_id)

    if not child_oid:
        return {"error": "ID inválido"}, 400

    child = mongo.db.children.find_one({"_id": child_oid})

    if not child:
        return {"error": "Criança não encontrada"}, 404

    # -----------------------------------
    # VERIFICA SE JÁ CONCLUIU FASE HOJE
    # -----------------------------------

    now = datetime.now()

    start_of_day = datetime(
        now.year,
        now.month,
        now.day,
        0, 0, 0
    )

    end_of_day = datetime(
        now.year,
        now.month,
        now.day,
        23, 59, 59
    )

    already_completed_today = mongo.db.activities.find_one({
        "child": child_oid,
        "type": "phase_completed",
        "createdAt": {
            "$gte": start_of_day,
            "$lte": end_of_day
        }
    })

    should_increment_streak = not already_completed_today

    # -----------------------------------
    # ATUALIZA PROGRESSO
    # -----------------------------------

    update_progress(
        child_oid,
        data,
        increment_streak=should_increment_streak
    )

    # -----------------------------------
    # LOG DE ATIVIDADE
    # -----------------------------------

    create_activity(child_oid, "phase_completed", {
        "worldCode": data.get("worldCode"),
        "moduleCode": data.get("moduleCode"),
        "phaseCode": data.get("phaseCode"),
    })

    return {
        "message": "Fase concluída com sucesso",
    }, 200

def get_notifications(id):
    child_oid = convert_id(id)
    if not child_oid:
        return {'error': 'ID inválido'}, 400

    notifications = list(mongo.db.notifications.find({'child': child_oid}))
    if not notifications:
        return {"error": "Sem notificações para esse usuario"}, 404

    return mongo_to_dict(notifications), 200