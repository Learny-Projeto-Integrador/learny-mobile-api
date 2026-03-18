from api import mongo
from datetime import datetime

def update_progress(child_id, world_code, phase_code):
    progress = mongo.db.progress.find_one({"child": child_id})

    if not progress:
        mongo.db.progress.insert_one({
            "child": child_id,
            "completedPhases": 1,
            "worlds": [
                {
                    "worldCode": world_code,
                    "phases": [
                        {"phaseCode": phase_code, "completed": True}
                    ]
                }
            ]
        })
        return

    mongo.db.progress.update_one(
        {"child": child_id},
        {"$inc": {"completedPhases": 1}}
    )

def check_and_unlock_medals(child_id, world_code):
    progress = mongo.db.progress.find_one({"child": child_id})
    medals_unlocked = []

    completed = progress.get("completedPhases", 0)

    rules = [
        ("FIRST_PHASE", completed >= 1),
        ("THREE_PHASES", completed >= 3),
    ]

    for medal_code, condition in rules:
        if condition:
            exists = mongo.db.medals.find_one({
                "child": child_id,
                "medalId": medal_code
            })

            if not exists:
                mongo.db.medals.insert_one({
                    "child": child_id,
                    "medalId": medal_code,
                    "unlockedAt": datetime.utcnow()
                })

                medals_unlocked.append(medal_code)

    return medals_unlocked

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
        "createdAt": datetime.utcnow()
    })
