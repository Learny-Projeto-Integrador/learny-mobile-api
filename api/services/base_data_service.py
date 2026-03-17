from api import mongo

def insert_world_definitions():
    worlds = [
        {
            "code": "WORLD_1",
            "name": "Dino's Forest",
            "description": "Floresta do Dino",
            "order": 1,
            "phases": [
                {"code": "W1_PHASE_1", "name": "Fase 1", "order": 1},
                {"code": "W1_PHASE_2", "name": "Fase 2", "order": 2},
                {"code": "W1_PHASE_3", "name": "Fase 3", "order": 3},
            ]
        },
        {
            "code": "WORLD_2",
            "name": "Jigsaw World",
            "description": "Mundo quebra-cabeça",
            "order": 2,
            "phases": [
                {"code": "W2_PHASE_1", "name": "Fase 1", "order": 1},
            ]
        },
        {
            "code": "WORLD_3",
            "name": "Space Realm",
            "description": "Reino Espacial",
            "order": 3,
            "phases": []
        },
        {
            "code": "WORLD_4",
            "name": "Pop Party",
            "description": "Festa Pop",
            "order": 4,
            "phases": []
        },
    ]

    for world in worlds:
        mongo.db.world_definitions.update_one(
            {"code": world["code"]},
            {"$setOnInsert": world},
            upsert=True
        )

def insert_medal_definitions():
    medals = [
        {
            "code": "FIRST_PHASE",
            "name": "Iniciando!",
            "description": "Você concluiu a fase 01",
            "worldCode": "WORLD_1"
        },
        {
            "code": "THREE_PHASES",
            "name": "A todo o vapor!",
            "description": "Você concluiu 3 fases",
            "worldCode": "WORLD_1"
        },
        {
            "code": "WORLD_1_COMPLETE",
            "name": "Desvendando",
            "description": "Você concluiu o mundo 01",
            "worldCode": "WORLD_1"
        },
    ]

    for medal in medals:
        mongo.db.medal_definitions.update_one(
            {"code": medal["code"]},
            {"$setOnInsert": medal},
            upsert=True
        )

def insert_mission_definitions():
    missions = [
        {
            "code": "COMPLETE_PHASE_1",
            "name": "Iniciando!",
            "description": "Conclua a fase 01",
            "worldCode": "WORLD_1",
        },
        {
            "code": "COMPLETE_3_PHASES",
            "name": "A todo o vapor!",
            "description": "Conclua 3 fases",
            "worldCode": "WORLD_1"
        },
        {
            "code": "COMPLETE_WORLD_1",
            "name": "Desvendando",
            "description": "Conclua o mundo 01",
            "worldCode": "WORLD_1"
        },
    ]

    for mission in missions:
        mongo.db.mission_definitions.update_one(
            {"code": mission["code"]},
            {"$setOnInsert": mission},
            upsert=True
        )

def insert_base_data():
    insert_world_definitions()
    insert_medal_definitions()
    insert_mission_definitions()
    



