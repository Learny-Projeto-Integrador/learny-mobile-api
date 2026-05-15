from api import mongo
from datetime import datetime

def update_progress(child_id, data, increment_streak=False):
    progress = mongo.db.progress.find_one({"child": child_id})

    phase_data = {
        "phaseCode": data.get("phaseCode"),
        "time": data.get("time"),
        "points": data.get("points"),
        "percentage": data.get("percentage"),
        "completed": True
    }

    # -----------------------------------
    # SOMA PONTOS, MOEDAS E STREAK (CASO SEJA A PRIMEIRA DO DIA)
    # -----------------------------------

    inc_data = {
        "points": data.get("points"),
        "coins": data.get("coins"),
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

    for world in worlds:
        if world["worldCode"] == data.get("worldCode"):
            world_found = True

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

            # Se o mundo existe mas a fase não
            if not phase_found:
                mongo.db.progress.update_one(
                    {
                        "child": child_id,
                        "worlds.worldCode": data.get("worldCode")
                    },
                    {
                        "$push": {
                            "worlds.$.completedPhases": phase_data
                        },
                    }
                )

            break

    # Se o mundo não existe
    if not world_found:
        mongo.db.progress.update_one(
            {"child": child_id},
            {
                "$push": {
                    "worlds": {
                        "worldCode": data.get("worldCode"),
                        "completedPhases": [phase_data]
                    }
                },
            }
        )

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
