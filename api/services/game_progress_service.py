from api import mongo
from datetime import datetime
        
def unlock_world_character(child_id, world_code):
    """
    Libera o personagem do mundo caso todas as fases tenham sido concluídas.
    """

    world_definition = mongo.db.world_definitions.find_one({
        "code": world_code
    })

    if not world_definition:
        return

    reward_character_code = world_definition.get("rewardCharacterCode")

    if not reward_character_code:
        return

    progress = mongo.db.progress.find_one({"child": child_id})

    if not progress:
        return

    world_progress = next(
        (
            world
            for world in progress.get("worlds", [])
            if world.get("worldCode") == world_code
        ),
        None
    )

    if not world_progress:
        return

    completed_phases = world_progress.get("completedPhases", [])

    completed_codes = [
        phase.get("phaseCode")
        for phase in completed_phases
        if phase.get("completed")
    ]

    # -----------------------------------
    # BUSCA TODOS OS MODULES DO MUNDO
    # -----------------------------------

    modules = list(
        mongo.db.module_definitions.find({
            "worldCode": world_code
        })
    )

    module_codes = [module["code"] for module in modules]

    # -----------------------------------
    # BUSCA TODAS AS FASES DO MUNDO
    # -----------------------------------

    phases = list(
        mongo.db.phase_definitions.find({
            "moduleCode": {
                "$in": module_codes
            }
        })
    )

    total_phase_codes = [
        phase["code"]
        for phase in phases
    ]

    # -----------------------------------
    # VERIFICA SE COMPLETOU TODAS
    # -----------------------------------

    world_completed = all(
        phase_code in completed_codes
        for phase_code in total_phase_codes
    )

    if not world_completed:
        return

    # -----------------------------------
    # EVITA DUPLICAR PERSONAGEM
    # -----------------------------------

    already_unlocked = any(
        character.get("characterCode") == reward_character_code
        for character in progress.get("characters", [])
    )

    if already_unlocked:
        return

    # -----------------------------------
    # LIBERA PERSONAGEM
    # -----------------------------------

    mongo.db.progress.update_one(
        {"child": child_id},
        {
            "$push": {
                "characters": {
                    "characterCode": reward_character_code,
                    "level": 1,
                    "characterPoints": 0,
                    "unlockedAt": datetime.utcnow()
                }
            },
            "$set": {
                "selectedCharacter": reward_character_code
            }
        }
    )
    
def update_progress(child_id, data, increment_streak=False):
    progress = mongo.db.progress.find_one({"child": child_id})

    if not progress:
        return {
            "error": "Progresso não encontrado"
        }, 404

    phase_data = {
        "phaseCode": data.get("phaseCode"),
        "time": data.get("time"),
        "points": data.get("points"),
        "percentage": data.get("percentage"),
        "completed": True
    }

    # -----------------------------------
    # SOMA PONTOS, MOEDAS E STREAK
    # -----------------------------------

    inc_data = {
        "points": data.get("points", 0),
        "coins": data.get("coins", 0),
    }

    if increment_streak:
        inc_data["streak"] = 1

    mongo.db.progress.update_one(
        {"child": child_id},
        {
            "$inc": inc_data
        }
    )

    progress = mongo.db.progress.find_one({"child": child_id})

    worlds = progress.get("worlds", [])

    world_found = False
    phase_found = False
    added_new_phase = False

    # -----------------------------------
    # PROCURA MUNDO
    # -----------------------------------

    for world in worlds:
        if world["worldCode"] == data.get("worldCode"):
            world_found = True

            # -----------------------------------
            # PROCURA FASE
            # -----------------------------------

            for phase in world.get("completedPhases", []):
                if phase["phaseCode"] == data.get("phaseCode"):
                    phase_found = True

                    # Atualiza fase existente
                    mongo.db.progress.update_one(
                        {
                            "child": child_id,
                            "worlds.worldCode": data.get("worldCode"),
                            "worlds.completedPhases.phaseCode": data.get("phaseCode")
                        },
                        {
                            "$set": {
                                "worlds.$[world].completedPhases.$[phase].time": data.get("time"),
                                "worlds.$[world].completedPhases.$[phase].points": data.get("points"),
                                "worlds.$[world].completedPhases.$[phase].percentage": data.get("percentage"),
                                "worlds.$[world].completedPhases.$[phase].completed": True
                            }
                        },
                        array_filters=[
                            {"world.worldCode": data.get("worldCode")},
                            {"phase.phaseCode": data.get("phaseCode")}
                        ]
                    )

                    break

            # -----------------------------------
            # MUNDO EXISTE MAS FASE NÃO
            # -----------------------------------

            if not phase_found:
                mongo.db.progress.update_one(
                    {
                        "child": child_id,
                        "worlds.worldCode": data.get("worldCode")
                    },
                    {
                        "$push": {
                            "worlds.$.completedPhases": phase_data
                        }
                    }
                )

                added_new_phase = True

            break

    # -----------------------------------
    # MUNDO NÃO EXISTE
    # -----------------------------------

    if not world_found:
        mongo.db.progress.update_one(
            {"child": child_id},
            {
                "$push": {
                    "worlds": {
                        "worldCode": data.get("worldCode"),
                        "percentage": data.get("percentage", 0),
                        "unlocked": True,
                        "completedPhases": [phase_data]
                    }
                }
            }
        )

        added_new_phase = True
        
    # -----------------------------------
    # RECALCULA PORCENTAGEM DO MUNDO
    # -----------------------------------

    modules = list(
        mongo.db.module_definitions.find({
            "worldCode": data.get("worldCode")
        })
    )

    module_codes = [
        module.get("code")
        for module in modules
    ]

    total_phases = mongo.db.phase_definitions.count_documents({
        "moduleCode": {
            "$in": module_codes
        }
    })

    # Busca progresso atualizado
    updated_progress = mongo.db.progress.find_one({
        "child": child_id
    })

    completed_count = 0

    for world in updated_progress.get("worlds", []):
        if world["worldCode"] == data.get("worldCode"):

            completed_count = len([
                phase
                for phase in world.get("completedPhases", [])
                if phase.get("completed")
            ])

            break

    percentage = 0

    if total_phases > 0:
        percentage = int(
            (completed_count / total_phases) * 100
        )

    # Atualiza porcentagem do mundo
    mongo.db.progress.update_one(
        {
            "child": child_id,
            "worlds.worldCode": data.get("worldCode")
        },
        {
            "$set": {
                "worlds.$.percentage": percentage
            }
        }
    )

    # -----------------------------------
    # VERIFICA DESBLOQUEIO DE PERSONAGEM
    # -----------------------------------

    if added_new_phase:
        unlock_world_character(
            child_id,
            data.get("worldCode")
        )
        
        return {
            "message": "Progresso atualizado com sucesso",
            "reward": "Novo pesronagem desbloqueado"
        }, 200

    return {
        "message": "Progresso atualizado com sucesso"
    }, 200

def check_missions(child_id, phase_code):
    mission = mongo.db.missions.find_one({
        "child": child_id,
        "completed": False,
        "title": {"$regex": phase_code, "$options": "i"}
    })

    if not mission:
        return None, 0

    mongo.db.missions.update_one(
        {"_id": mission["_id"]},
        {"$set": {"completed": True}}
    )

    bonus = 50

    return {
        "mission": mission["title"],
        "bonus": bonus
    }, bonus

def create_activity(child_id, type, data):
    mongo.db.activities.insert_one({
        "child": child_id,
        "type": type,
        "data": data,
        "createdAt": datetime.now()
    })
